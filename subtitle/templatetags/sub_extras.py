from django import template

from search import models as search_modules
from subtitle import models as sub_models

register = template.Library()


@register.filter(name='multiply')
def multiply(value, arg):
    if value == "" or value == None:
        value = 0
    return int(value * arg)


@register.filter(name="divide")
def divide(value, arg):
    return int(value / arg)


@register.filter(name="get_genre")
def get_genre(value):
    value = int(value)
    return search_modules.GenreDB.objects.get(id=value)


@register.filter(name="get_color")
def get_color(value):
    COLOR = (
        "red",
        'orange',
        'amber',
        'yellow text-white',
        'lime text-white',
        'light-green',
        'teal',
        'cyan',
        'blue',
        'indigo'
    )
    class_str = ""

    for i in range(0, 10):
        if value > i:
            class_str = COLOR[i]
    return class_str


import time


@register.filter(name='strftime')
def strftime(value):
    if value == None or value == "":
        value = 0
    return time.strftime("%H:%M:%S", time.gmtime(value * 60))


@register.filter(name="flag")
def flag(value):
    FLAG = sub_models.FLAG

    return FLAG[value]
