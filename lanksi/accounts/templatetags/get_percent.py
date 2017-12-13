from django import template

register = template.Library()


@register.filter
def subtract(value, arg):
    return value - arg

@register.filter
def get_percent(value, arg):
    return value / arg * 100