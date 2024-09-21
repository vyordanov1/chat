from django import template

register = template.Library()


@register.filter(name='remove_hyphens')
def remove_hyphens(value):
    return str(value).replace('-', '')