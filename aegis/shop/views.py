from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST

from .models import Сategories, Products, Account, Purchases


from .cart import Cart
from .forms import CartAddPurchasesForm


@require_POST
def cart_add(request, purchases_id):
    cart = Cart(request)
    purchase = get_object_or_404(Purchases, id=purchases_id)
    form = CartAddPurchasesForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        cart.add(purchase=purchase,
                 quantity=cd['quantity'])
    return redirect('cart:cart_detail')


def cart_remove(request, purchases_id):
    cart = Cart(request)
    purchase = get_object_or_404(Purchases, id=purchases_id)
    cart.remove(purchase)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddPurchasesForm(initial={'quantity': item['quantity'],
                                                                   'update': True})
    return render(request, 'shop/order.html', {'cart': cart})


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
    if request.method == 'POST':
        form = CartAddPurchasesForm(request.POST)
        if form.is_valid():
            p = Purchases()
            p.product = product
            p.quantity = request.POST['quantity']
            p.size = request.POST['size']
            p.save()
            return redirect('home')

    form = CartAddPurchasesForm()

    return render(request, 'shop/Shop-buy.html', {'product': product, 'form': form})


def buy_success(request, product):
    p = Purchases()
    p.product = product
    p.quantity = request.POST['quantity']
    p.size = request.POST['size']
    p.save()

    return reverse_lazy('home')


