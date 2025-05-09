import re
from django import template

register = template.Library()

@register.filter
def regex_search(value, pattern):
    return re.search(pattern, str(value)) is not None