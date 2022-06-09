from django.urls import include, path

from .views import Dashboard, GiveHelp, ReceiveHelp
app_name='myapp'

urlpatterns = [
	path('', Dashboard.as_view(), name='dashboard'),
	path('givehelp/', GiveHelp.as_view(), name='givehelp'),
	# admin view for a user
	path('givehelp/<int:username>/', GiveHelp.as_view(), name='givehelp'),
	
	path('receivehelp/', ReceiveHelp.as_view(), name='receivehelp'),
	
]
