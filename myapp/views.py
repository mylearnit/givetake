
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
    def get(self, request):
        ancestors = BinaryTree.objects.get(pk=request.user.username).get_ancestors()[:10]
        return render(request,'myapp/givehelp.html',{'ancestors':ancestors})

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