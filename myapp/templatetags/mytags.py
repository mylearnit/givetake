from django import template
from myapp.models import BinaryTree, PaymentDetails

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def not_paid_to(sel_user, ancestor):
    if PaymentDetails.objects.filter(binarytree_id=sel_user.username, user=ancestor.user, is_paid=True):
        return False # paid
    return True # not paid
