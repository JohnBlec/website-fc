from django.shortcuts import render, get_object_or_404
from .models import Сategories, Products

def shop(request):
    products = Products.objects.order_by('id')
    return render(request, 'shop/Shop.html', {'products': products})

def show_category(request, category_slug):
    category = get_object_or_404(Сategories, slug=category_slug)
    category_id = category.pk
    products = Products.objects.filter(cat_id=category_id)

    return render(request, 'shop/Shop_category.html', {'products': products, 'category': category})

def buy(request, product_slug):
    product = get_object_or_404(Products, slug=product_slug)

    return render(request, 'shop/Shop-buy.html', {'product': product})
