from django import template
from shop.models import Сategories

register = template.Library()

@register.inclusion_tag('shop/list_categories.html')
def show_categories():
    cats = Сategories.objects.order_by('id')

    return {"cats": cats}