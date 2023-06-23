from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('category/<slug:category_slug>', views.show_category, name='category'),
    path('product/<slug:product_slug>', views.buy, name='product'),
    path('cart', views.cart, name='cart'),
    path('remove/<str:purchases_id>/<str:user_id>', views.remove_purchases, name='remove'),
]
