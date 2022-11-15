from django import forms
from django.forms import ModelForm

from shop.models import Purchases




class CartAddPurchasesForm(ModelForm):

    class Meta:
        model = Purchases

        PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 11)]

        SIZE_SELECTION = [
            ('XS', 'XS'),
            ('S', 'S'),
            ('M', 'M'),
            ('L', 'L'),
            ('XL', 'XL'),
            ('XXL', 'XXL'),
            ('3XL', '3XL')
        ]

        fields = ['quantity', 'size']

        widgets = {
            "quantity": forms.Select(
                                choices=PRODUCT_QUANTITY_CHOICES,
                                ),
            "size": forms.Select(choices=SIZE_SELECTION),
        }
