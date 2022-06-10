from django import template
from myapp.models import BinaryTree

register = template.Library()

@register.filter
def index(indexable, i):
    return indexable[i]


@register.filter
def payment_done(user, level):
    # check nusra(level 2) pay sumesh(level 1), 
    # then sumee(request.user) and sofi profile page will show nusra(level 2)
    
    # check nusra(user) payed her level sumesh. so to show gpay in sumee page
    mynode = BinaryTree.objects.get(pk=user.username) # nusra
    if mynode.depth == 1: return True # if root user, then always return True

    payment_done_users = mynode.is_paid.all()
    ancestors = mynode.get_ancestors()[:10][::-1]
    
    for i in range(1,10):
        # i don't know why i used range(1,10)
        if mynode.depth == (i+1):
            # check he paid to user with depth i
            if ancestors[-i].user in payment_done_users:
                return True

    if ancestors[level].user in payment_done_users:
        return True
    return False
