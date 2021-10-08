from django import template
register = template.Library()


@register.filter
def index(indexable, i: int = 0):
    return indexable[i]
