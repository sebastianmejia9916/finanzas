# yourapp/templatetags/custom_filters.py

from django import template

register = template.Library()

@register.filter
def thousand_separator(value):
    return '{:,.3f}'.format(value)
