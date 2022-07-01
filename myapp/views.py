
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect

from django.forms import ModelForm
from django.views.generic import CreateView
from django.contrib.auth import login

from myapp.models import BinaryTree, PaymentDetails
from adminapp.views import givehelp_ancestors
from adminapp.givehelp_functions import GIVE_AMOUNTS,PMF, givehelp_ancestors, get_ancestors_and_payments

from .forms import SignUpForm
User = get_user_model()



class SignUpView(CreateView):
    model = User
    form_class = SignUpForm
    template_name = 'registration/signup_form.html'

    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return redirect('home')

def home(request):
    if request.user.is_superuser:
        return redirect('adminapp:paymentdone_requests')
        
    elif request.user.is_authenticated:
        return redirect('myapp:dashboard')
    return redirect('login')

@method_decorator([login_required], name='dispatch')
class Dashboard(View):
    def get(self, request):
        return render(request,'myapp/dashboard.html')

@method_decorator([login_required], name='dispatch')
class ReceiveHelp(View):
    def get(self, request):
        # find stages of tree
        stage = int(request.GET.get('stage',1))
        
        mynode = BinaryTree.objects.get(pk=request.user.username)
        descendants = mynode.get_descendants()
        stage_nodes = []
        for descendant in descendants:
            if descendant.depth == mynode.depth+stage:
                stage_nodes.append(descendant)
        return render(request,'myapp/receivehelp.html',{
            'stage_nodes':stage_nodes,
            'stage':stage,
            'amts':GIVE_AMOUNTS
            })

@method_decorator([login_required], name='dispatch')
class ReceiveHelpChart(View):
    def get(self, request):
        payments = PaymentDetails.objects.filter(binarytree_id=request.user.username,is_paid=True)

        stages = []
        stages_status = [] # how many persons paid in each stage
        n = 2
        for i in range(10):
            stages.append(n)
            n=n*2


        return render(request,'myapp/receivehelp_chart.html',{'amts':GIVE_AMOUNTS, 'stages':stages})

@method_decorator([login_required], name='dispatch')
class GiveHelp(View):
    def post(self, request):
        node = BinaryTree.objects.get(id=request.user.username)
        to_user = User.objects.get(username = request.POST.get('to_user'))
        payment, _ = PaymentDetails.objects.get_or_create(
            user = to_user,binarytree=node)
        payment.payment_done_requested = True
        payment.screenshotfile = request.FILES.get('screenshotfile',None)
        payment.save()
        return redirect('myapp:givehelp') # HttpResponseRedirect(reverse('myapp.views.list'))

    def payments_to_be_done(self,unpaid_node, stage):
        # if recieve amount greater than 4200,
        # pay 5th stage ie(1220rs)
        # 3240 = 1300+720(pmf)+800+420(pmf)
        
        
        paid = unpaid_node.user.total_give_help + unpaid_node.user.total_pmf
        print(paid,unpaid_node.user.first_name)
        payments_required = {3240:[4200,5]}#{5:[3240,4200],}
        if unpaid_node.user.total_received_help > payments_required[paid][0]:
            
            if paid < payments_required[stage][0]:
                return False
        return True

    def get_last_ancestor_paid(self, unpaid_node, no_of_ancestors):
        """
        unpaid_node is the last ancestor with index eg 4(no_of_ancestors).
        now this last ancestor will have ancestors, sometimes length 2
        """
        # last node is maybe unpaid node, every other ancestor is paid
        unpaid_node_ancestors, payment_done_users = get_ancestors_and_payments(unpaid_node)
        
        if no_of_ancestors <= len(unpaid_node_ancestors):
            print(no_of_ancestors, len(unpaid_node_ancestors))
            # last node is the unpaidnode_ancestor
            above_node= unpaid_node_ancestors[no_of_ancestors-1]
            if above_node.user in payment_done_users:
                # return True
                return self.payments_to_be_done(unpaid_node, no_of_ancestors)
            else:
                return False
        else:
            # i didn't think about it much
            print('index:', no_of_ancestors-1, unpaid_node, unpaid_node_ancestors, payment_done_users)
            root_node = BinaryTree.get_first_root_node()
            if unpaid_node == root_node:
                # root node doesn't required to pay to any one.
                return True
            # check root node in payment_done_users
            print(root_node.user, payment_done_users)
            if root_node.user in payment_done_users:
                # return True
                return self.payments_to_be_done(unpaid_node, no_of_ancestors)
            
            return False

    def get(self, request):
        self.user = request.user
        mynode = BinaryTree.objects.get(pk=request.user.username)
        ancestors = givehelp_ancestors(mynode)

        no_of_ancestors = len(ancestors)
        is_last_ancestor_paid = True # for root node there is no ancestors
        if no_of_ancestors>0:
            # if nusra pay arun, then sumee and other profile page will show nusra
            
            is_last_ancestor_paid = self.get_last_ancestor_paid(ancestors[-1], no_of_ancestors)
        
        return render(request,'myapp/givehelp.html',{
            'amts': GIVE_AMOUNTS, 
            'pmfs':PMF,
            'is_last_ancestor_paid': is_last_ancestor_paid,
            'ancestors':ancestors
            })

@method_decorator([login_required], name='dispatch')
class Profile(View):
    # even inactive users can view/edit their profile
    def get(self, request):
        return render(request,'registration/profile.html')

    def post(self,request):
        # user_id=request.POST['user']
        user = request.user #User.objects.get(id = user_id)
        
        user.first_name = request.POST.get('first_name','')
        # user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, f'User details of {user.username} saved with success!')
        return redirect('profile')