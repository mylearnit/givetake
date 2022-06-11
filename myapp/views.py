
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from myapp.models import BinaryTree, PaymentDetails

from django.forms import ModelForm
from django.views.generic import CreateView
from django.contrib.auth import login
from .forms import SignUpForm
User = get_user_model()

GIVE_AMOUNTS = [150,200,400,600,800,1000,2000,3000,4000,5000]

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
        return redirect('adminapp:home')
        
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
class GiveHelp(View):
    def givehelp_ancestors(self, mynode):
        # get last 10 ancestors and reverse it
        ancestors = mynode.get_ancestors()[::-1][:10]
        payment_done_users = [payment.user for payment in PaymentDetails.objects.filter(binarytree=mynode,is_paid=True)] # mynode.payment.all()
        # what if there is less than 10 ancestors
        filtered_ancestors = []
        for ancestor in ancestors:
            filtered_ancestors.append(ancestor)
            if ancestor.user not in payment_done_users:
                break
            
        return filtered_ancestors

    def get_last_ancestor_paid(self, ancestors):
        # last node is maybe unpaid node, every other ancestor is paid
        unpaid_node = ancestors[-1]
        payment_done_users = [payment.user for payment in PaymentDetails.objects.filter(binarytree=unpaid_node,is_paid=True)] # unpaid_node.payment.all()

        unpaid_node_ancestors = unpaid_node.get_ancestors()[::-1][:10]

        
        if len(ancestors) <= len(unpaid_node_ancestors):
            print(len(ancestors), len(unpaid_node_ancestors))
            # last node is the unpaidnode_ancestor
            above_node= unpaid_node_ancestors[len(ancestors)-1]
            if above_node.user in payment_done_users:
                return True
            else:
                return False
        else:
            # i didn't think about it much
            print('index:', len(ancestors)-1, unpaid_node, unpaid_node_ancestors, payment_done_users)
            # check root node in payment_done_users
            print(BinaryTree.get_first_root_node().user, payment_done_users)
            if BinaryTree.get_first_root_node().user in payment_done_users:
                return True
            return False

    def get(self, request, username=None):
        
        context = {'amts': GIVE_AMOUNTS}
        if username:
            # if admin user
            template = 'adminapp/user.html'
            context['sel_user'] = User.objects.get(username=username)
            is_admin=True
        else:
            template = 'myapp/givehelp.html'
            username = request.user.username
            is_admin=False
            

        mynode = BinaryTree.objects.get(pk=username)
        ancestors = self.givehelp_ancestors(mynode)
        
        if not is_admin:
            # if not admin user
            is_last_ancestor_paid = True # for root node there is no ancestors
            if len(ancestors)>0:
                # if nusra pay arun, then sumee and other profile page will show nusra
                is_last_ancestor_paid = self.get_last_ancestor_paid(ancestors)
            context['is_last_ancestor_paid']= is_last_ancestor_paid
            print(is_last_ancestor_paid)
        context['ancestors'] = ancestors
        return render(request,template,context)

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