from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('category/<slug:category_slug>', views.show_category, name='category'),
    path('product/<slug:product_slug>', views.buy, name='product'),
]

