from django.urls import include, path

from .views import Dashboard, GiveHelp
app_name='myapp'

urlpatterns = [
	path('', Dashboard.as_view(), name='dashboard'),
	path('givehelp/', GiveHelp.as_view(), name='givehelp'),
]
