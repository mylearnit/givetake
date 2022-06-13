from myapp.models import PaymentDetails

GIVE_AMOUNTS = [150,200,400,600,800,1000,2000,3000,4000,5000]

def get_ancestors_and_payments(mynode):
    # get last 10 ancestors and reverse it
    ancestors = mynode.get_ancestors()[::-1][:10]
    payment_done_users = [payment.user for payment in PaymentDetails.objects.filter(binarytree=mynode,is_paid=True)]
    return (ancestors, payment_done_users)

def givehelp_ancestors(mynode):
    ancestors, payment_done_users = get_ancestors_and_payments(mynode)
    # what if there is less than 10 ancestors
    filtered_ancestors = []
    for ancestor in ancestors:
        filtered_ancestors.append(ancestor)
        if ancestor.user not in payment_done_users:
            break
        
    return filtered_ancestors
