from django.urls import path

from . import views

app_name = "products"

urlpatterns = [
	path('', views.IndexView.as_view(), name="all"),
	path('product/<int:pk>/detail/', views.ProductDetail.as_view(), name="detail"),
	path('cart/', views.CartView.as_view(), name="cart"),
	path('cart/<int:pk>/<str:command>/', views.cart, name="cart_exec"),
]