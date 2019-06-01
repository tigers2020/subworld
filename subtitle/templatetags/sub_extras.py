from django import template
from search import models

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    return int(value * arg)


@register.filter(name="divide")
def divide(value, arg):
    return int(value / arg)


@register.filter(name="get_genre")
def get_genre(value, args):
    return models.GenreDB.objects.get(id=value)

@register.filter(name="range")
def range(value):
    return range(value)