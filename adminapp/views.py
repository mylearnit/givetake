import uuid
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth import get_user_model
from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages


from myapp.models import BinaryTree, PaymentDetails
User = get_user_model()

class SuperAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_superuser

# Create your views here.
class Home(SuperAdminRequiredMixin,View):
    def create_user_and_tree(self, request, parent,name, mobile,gpay, email):
        """Create New BinaryTree"""
        user = User.objects.create_user(
            username = str(uuid.uuid4()), # just a temporary username
            password = '123456',
            first_name = name,
            mobile = mobile,
            gpay= gpay,
            email=email,
        )
        if parent=='0':
            obj = BinaryTree.add_root(user=user)
        else:
            obj = BinaryTree.objects.get(pk=parent).add_child(user=user)

        # users created using createadminuser/adminpage must be username with characters
        user.username = obj.id
        user.save()
        messages.success(request, f'Success: Tree of {user.first_name} created successfully.')

    def get(self, request):
        context = {
            'alist': BinaryTree.get_annotated_list_qs(
                BinaryTree.objects.all() # filter(user=request.user)
            )
        }
        return render(request,'adminapp/home.html',context)

    def post(self,request):
        
        parent = request.POST.get('parent_id')
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        gpay = request.POST.get('gpay')

        if all([parent,name,mobile,gpay]):
            if parent=='0':
                # if root
                self.create_user_and_tree(request, parent,name, mobile,gpay, email)
            elif BinaryTree.objects.filter(id=parent):
                if BinaryTree.objects.get(pk=parent).get_children_count()==2:
                    # Need to prevent more than 2 childs
                    messages.error(request,  'Error: Already has 2 child.')
                else:
                    self.create_user_and_tree(request, parent,name, mobile,gpay, email)
            else:
                messages.error(request,  'Error: Invalid Parent.')
        else:
            messages.error(request, 'Error: Parent, Name, Mobile and GPay is required.')
        return redirect(f"{reverse('adminapp:home')}")

class UserView(SuperAdminRequiredMixin,View):
    def post(self,request, username):
        """Change payment status"""
        
        # from_user = User.objects.get(username = request.POST.get('from_user'))
        to_user = User.objects.get(username = request.POST.get('paid_to'))
        payment_status = request.POST.get('payment_status')
        if payment_status=='paid':
            node = BinaryTree.objects.get(id=username)
            PaymentDetails.objects.get_or_create(user = to_user,binarytree=node, 
                defaults={'is_paid':True})
        messages.success(request, 'Success: Changed payment status.')
        return redirect(f"{reverse('myapp:givehelp', kwargs={'username': username})}")

        