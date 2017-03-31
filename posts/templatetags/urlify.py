import urllib.parse
from django import template

register = template.Library()

@register.filter

def urlify(value):
    return urllib.parse.quote_plus(value)