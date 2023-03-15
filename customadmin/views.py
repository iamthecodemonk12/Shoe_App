from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.views import generic
from django.urls import reverse_lazy

from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.hashers import check_password

from django.contrib import admin
from django.utils.decorators import method_decorator
from django.contrib.admin.views.decorators import staff_member_required


def user_has_permission(request): # user has logged in already
    return admin.site.has_permission(request)


def redirect(url, reverse=True):
    return HttpResponseRedirect(reverse_lazy(url) if reverse else url)
    

class BaseView(object):
    template_name = 'customadmin/index.html'
    
    def dispatch(self, request, *a, **kw):
        if not user_has_permission(request):
            return redirect('customadmin:login')
        return super().dispatch(request, *a, **kw)
    

class IndexView(BaseView, generic.TemplateView):
    pass


class LoginView(generic.TemplateView):
    template_name = "customadmin/login.html"
    
    def dispatch(self, request, *a, **kw):
        if user_has_permission(request):
            return redirect('customadmin:index')
        return super().dispatch(request, *a, **kw)
    
    
    def post(self, request, *a, **kw):
        username, password = request.POST.get('Username'), request.POST.get('Password')
        if not (username or password):
            return HttpResponse("Either the user name or password is not filled")
        try:
            user = User.objects.get(username=username)
            user_has_password = check_password(password, user.password)
            if not user_has_password:
                raise User.DoesNotExist('no password match')
            
            auth.login(request, user)
            
        except User.DoesNotExist as e:
            return render(request, self.template_name, {
                'error': True
            }) 
        return redirect('customadmin:index')


def logout(request):
    user = auth.get_user(request)
    auth.logout(request)
    return redirect('customadmin:login')
