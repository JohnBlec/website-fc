from django import template

register = template.Library()


@register.simple_tag
def fmonth(value):
    new_month = value
    return new_month
