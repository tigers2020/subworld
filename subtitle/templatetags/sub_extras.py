from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return value * arg


@register.filter(name="get_genre")
def get_genre(value, args):
    for arg in args:
        if arg.id == value:
            return arg.name
