from django import template

register = template.Library()


@register.simple_tag
def appropriation(value):
    new_month = value
    return new_month


@register.simple_tag
def addpos(value):
    new_pos = value + 1
    return new_pos
