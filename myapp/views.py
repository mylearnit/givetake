
# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from myapp.models import BinaryTree

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
class GiveHelp(View):
    def get(self, request, username=None):
        template = 'adminapp/user.html'
        if not username:
            # if not admin user
            template = 'myapp/givehelp.html'
            username = request.user.username
        
        mynode = BinaryTree.objects.get(pk=username)
        # get last 10 ancestors and reverse it
        ancestors = mynode.get_ancestors()[:10][::-1]
        payment_done_users = mynode.is_paid.all()

        # find next payment user
        next_payment_user = None
        for ancestor in ancestors:
            if ancestor.user not in payment_done_users:
                next_payment_user = ancestor.user
                break

        return render(request,template,{
            # i think sel_user is only required for admin user
            'sel_user':User.objects.get(username=username),
            'ancestors':ancestors,
            'payment_done_users':payment_done_users,
            'next_payment_user':next_payment_user,
            'amts':GIVE_AMOUNTS
            })

@method_decorator([login_required], name='dispatch')
class Profile(View):
    # even inactive users can view/edit their profile
    def get(self, request):
        return render(request,'registration/profile.html')

    def post(self,request):
        # user_id=request.POST['user']
        user = request.user #User.objects.get(id = user_id)
        """
        username = request.POST.get('username', '')
        if len(username) < 3:
            messages.error(request, 'Error: Username must have atleast 3 characters.')
            return redirect('profile')

        if username != user.username:
            if get_user_model().objects.filter(username=username).exists():
                messages.error(request, 'Error: Username already exists.')
                return redirect('profile')
            user.username = username    
        """
        
        user.first_name = request.POST.get('first_name','')
        # user.last_name = request.POST.get('last_name', '')
        user.email = request.POST.get('email', '')
        user.save()
        messages.success(request, f'User details of {user.username} saved with success!')
        return redirect('profile')