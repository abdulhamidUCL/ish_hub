from django import template
from ..models import *

register = template.Library()

@register.simple_tag()
def get_sorters():
    return {
        "new": "Newest",
        "old": "Oldest",
        "a-z": "A-Z",
        "z-a": "Z-A",
    }