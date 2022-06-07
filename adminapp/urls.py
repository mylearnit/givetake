from django.urls import include, path

from .views import Home, UserView
app_name='adminapp'

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('user/<int:username>', UserView.as_view(), name='user'),
]

