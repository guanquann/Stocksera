from django import template

register = template.Library()


@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def to_replace(value):
    return value.replace("1", "")


@register.filter
def get_range(value):
    return range(value)


@register.filter(name='split')
def split(value, key):
    value.split("key")
    return value.split(key)
