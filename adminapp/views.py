
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views import View

from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from django.db.models import Max
from myapp.forms import User

from myapp.models import BinaryTree


from django.contrib.auth.mixins import UserPassesTestMixin


class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

# Create your views here.
class Home(SuperAdminRequiredMixin,View):
    def get(self, request):
        context = {
            'alist': BinaryTree.get_annotated_list_qs(
                BinaryTree.objects.all() # filter(user=request.user)
            )
        }
        return render(request,'adminapp/home.html',context)

    def post(self,request):
        """Create New BinaryTree"""
        User = get_user_model()
        parent = request.POST.get('parent_id')
        if parent=='0':
            # if root no need to create User, so first name not required
            BinaryTree.add_root(user=request.user)
            messages.success(request, 'Success: Root Tree created successfully.')

        elif parent and request.POST.get('name'):
            print(request.user.id, parent)
            if BinaryTree.objects.filter(id=parent):
                if BinaryTree.objects.get(pk=parent).get_children_count()==2:
                    # Need to prevent more than 2 childs
                    messages.error(request,  'Error: Already has 2 child.')
                else:
                    user = User.objects.create_user(
                        username = User.objects.aggregate(m=Max('id'))['m'] + 1, # just a temporary username
                        password = '123456',
                        first_name = request.POST.get('name')
                    )
                    obj = BinaryTree.objects.get(pk=parent).add_child(user=user)

                    # users created using createadminuser/adminpage must be username with characters
                    user.username = obj.id
                    user.save()
                    messages.success(request, f'Success: Tree of {user.first_name} created successfully.')
                
            else:
                messages.error(request,  'Error: Invalid Parent.')
        else:
            messages.error(request, 'Error: Parent and Name is required.')
        return redirect(f"{reverse('adminapp:home')}")




class UserView(SuperAdminRequiredMixin,View):
    def get(self, request, username):
        ancestors = BinaryTree.objects.get(pk=username).get_ancestors()[:10]
        return render(request,'adminapp/user.html',{'sel_user':User.objects.get(username=username),'ancestors':ancestors})