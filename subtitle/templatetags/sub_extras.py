from django import template

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return int(value * arg)


@register.filter(name="divide")
def divide(value, arg):
    return int(value / arg)


@register.filter(name="get_genre")
def get_genre(value, args):

    for arg in args['genres']:
        if arg['id'] == value:
            return arg['name']

@register.filter(name="range")
def range(value):
    return range(value)