from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms
from myapp.models import BinaryTree
User = get_user_model()

class SignUpForm(UserCreationForm):
    parent = forms.CharField(
        required=True
    )
    class Meta(UserCreationForm.Meta):
        model = User

     
    def save(self):
        user = super().save(commit=False)
        user.save()
        obj = BinaryTree.objects.get(pk=self.cleaned_data.get('parent')).add_child(user=user)

        return user
