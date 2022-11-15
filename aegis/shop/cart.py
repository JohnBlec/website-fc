from decimal import Decimal
from django.conf import settings
from .models import Purchases


class Cart(object):

    def __init__(self, request):
        """
        Инициализация корзины
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем ПУСТУЮ корзину в сессии
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем товары из базы данных.
        """
        purchase_ids = self.cart.keys()
        # получаем товары и добавляем их в корзину
        purchases = Purchases.objects.filter(id__in=purchase_ids)

        cart = self.cart.copy()
        for purchase in purchases:
            cart[str(purchase.id)]['purchase'] = purchase

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """
        Считаем сколько товаров в корзине
        """
        return sum(item['quantity'] for item in self.cart.values())

    def add(self, purchases, quantity=1):
        """
        Добавляем товар в корзину или обновляем его количество.
        """
        purchase_id = str(purchases.id)
        if purchase_id not in self.cart:
            self.cart[purchase_id] = {'quantity': 0,
                                     'price': str(purchases.price)}

        self.cart[purchase_id]['quantity'] = quantity

        self.save()

    def save(self):
        # сохраняем товар
        self.session.modified = True

    def remove(self, purchase):
        """
        Удаляем товар
        """
        purchase_id = str(purchase.id)
        if purchase_id in self.cart:
            del self.cart[purchase_id]
            self.save()

    def get_total_price(self):
        # получаем общую стоимость
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        # очищаем корзину в сессии
        del self.session[settings.CART_SESSION_ID]
        self.save()