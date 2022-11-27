from django.contrib import admin
from .models import Сategories,  Kinds, Products, Orders, Purchases

admin.site.register(Сategories)
#admin.site.register(Account)
admin.site.register(Kinds)
admin.site.register(Products)
admin.site.register(Orders)
admin.site.register(Purchases)
