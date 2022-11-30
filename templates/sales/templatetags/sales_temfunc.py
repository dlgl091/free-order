from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def truncate_mf(value):
    if value.find(',') != -1:
        return value[:value.find(',')]
