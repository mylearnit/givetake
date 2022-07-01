from django import template
from myapp.models import BinaryTree, PaymentDetails

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]

@register.filter
def paid_to_user(sel_user, user):
    if PaymentDetails.objects.filter(binarytree_id=sel_user.username, user=user, is_paid=True):
        return True # paid
    return False # not paid

@register.filter
def paid_to(sel_user, ancestor):
    if PaymentDetails.objects.filter(binarytree_id=sel_user.username, user=ancestor.user, is_paid=True):
        return True # paid
    return False # not paid

@register.filter
def paid_requested(sel_user, ancestor):
    if PaymentDetails.objects.filter(binarytree_id=sel_user.username, user=ancestor.user, payment_done_requested=True):
        return True # paid
    return False # not paid

@register.filter
def get_screenshot(user, ancestor):
    payment = PaymentDetails.objects.filter(binarytree_id=user.username, user=ancestor.user, payment_done_requested=True)
    if payment and payment.first().screenshotfile:
        return payment.screenshotfile.url
    return ''


# @register.simple_tag
# def define(val=None):
#   return val