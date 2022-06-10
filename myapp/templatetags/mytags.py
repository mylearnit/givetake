from django import template
from myapp.models import BinaryTree

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]
