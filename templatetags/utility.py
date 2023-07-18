# templatetags/cut_re.py
import re 
from django import template

register = template.Library()

@register.filter
def cut_re(value, search): 
    return re.sub(search, "", value)


@register.filter
def split(value, key):
    return value.split(key)






