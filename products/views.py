from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic import (
    TemplateView, ListView, DetailView
    )

from .models import Product


def bug(msg=":)"):
    raise Exception(msg)


g04 = get_object_or_404

class BaseView():
    template_name = "products/index.html"
    model = Product
    context_object_name = 'products'

    def get_context_data(self, *a, **kw):
        context = super().get_context_data(*a, **kw)
        context.update({
            "cart": [ [g04(Product, id=product_id), quantity] for product_id, quantity in self.get_cart().items()]
        })
        return context

    def get_cart(self, request=None):
        request = request or self.request
        self.request = request
        if not request.session.get('cart') or type(request.session['cart']) != dict:
            request.session['cart'] = {}
        return request.session['cart']


class MainView(BaseView, TemplateView):
    pass


class IndexView(BaseView, ListView):
    paginate_by = 30

    def get_queryset(self, *a, **kw):
        # fake some random items from db : duplicate randomly
        def get():
            import random
            products = self.model.objects.all()
            if not products:
                return
            for _ in range(30 * 3 + 5):
                yield random.choice(products)
        results = list(get())
        if results:
            self.has_results = True
        return results

class ProductDetail(BaseView, generic.DetailView):
    template_name = "products/product_detail.html"
    context_object_name = 'product'


class CartView(IndexView):
    template_name = "products/cart.html"


def cart(request, pk, command):
    # stry:
    product_id = str(Product.objects.get(id=pk).id)
    cart = request.session['cart']
    if command == 'add':
        try:
            cart[product_id] += 1
        except KeyError:
            cart[product_id] = 1
    elif command == 'del':
        try:
            del cart[product_id]
        except KeyError:
            pass
    request.session.modified = True
    return HttpResponseRedirect('/products/cart/')
