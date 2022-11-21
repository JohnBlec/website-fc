from django.shortcuts import render, get_object_or_404, redirect
from .models import Сategories, Products, Account, Purchases, Orders
from .forms import CartAddPurchasesForm, СompletionPurchaseForm


def shop(request):
    products = Products.objects.order_by('id')
    return render(request, 'shop/Shop.html', {'products': products})


def show_category(request, category_slug):
    category = get_object_or_404(Сategories, slug=category_slug)
    category_id = category.pk
    products = Products.objects.filter(cat_id=category_id)
    return render(request, 'shop/Shop_category.html', {'products': products, 'category': category})


def buy(request, product_slug, user_id):
    product = get_object_or_404(Products, slug=product_slug)
    if request.method == 'POST':
        form = CartAddPurchasesForm(request.POST)
        if form.is_valid():
            if Account.objects.filter(pk=user_id):
                account = Account.objects.get(pk=user_id)
                if Orders.objects.filter(account_id=user_id, status=False):
                    ords = Orders.objects.get(account_id=user_id, status=False)
                    p = Purchases()
                    p.product = product
                    p.quantity = request.POST['quantity']
                    p.size = request.POST['size']
                    p.order = ords
                    p.save()
                    return redirect('cart', user_id)
                else:
                    o = ord_creat(account)
                    p = Purchases()
                    p.product = product
                    p.quantity = request.POST['quantity']
                    p.size = request.POST['size']
                    p.order = o
                    p.save()
                    return redirect('cart', user_id)
            else:
                return redirect('singIn')

    form = CartAddPurchasesForm()

    return render(request, 'shop/Shop-buy.html', {'product': product, 'form': form})


def cart(request, user_id):
    error = ''

    if request.method == 'POST':
        form = СompletionPurchaseForm(request.POST)
        if form.is_valid():
            ords = Orders.objects.get(account_id=user_id, status=False)
            ords.phone_number = request.POST['phone_number']
            ords.status = True
            ords.save()
        else:
            error = 'Неправильно написали номер телефона!'

    if not Orders.objects.filter(account_id=user_id, status=False):
        account = Account.objects.get(pk=user_id)
        ord_creat(account)

    user_cart = Orders.objects.get(account_id=user_id, status=False)

    purchases = Purchases.objects.filter(order_id=user_cart.pk)

    total_price = sum_price_products(purchases)

    form = СompletionPurchaseForm()

    return render(request, 'shop/Order.html', {'purchases': purchases,
                                               'total_price': total_price,
                                               'form': form,
                                               'error': error})


def remove_purchases(request, purchases_id, user_id):
    p = Purchases.objects.get(pk=purchases_id)
    p.delete()
    return redirect('cart', user_id)


def sum_price_products(purchases):
    sum_price = 0
    for pr in purchases:
        sum_price += pr.quantity * pr.product.price
    return sum_price


def ord_creat(user):
    o = Orders()
    o.account = user
    o.status = False
    o.save()
    return o
