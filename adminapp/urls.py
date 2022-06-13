from django.urls import include, path

from .views import Home, UserView, PaymentDoneView
app_name='adminapp'

urlpatterns = [
	path('', Home.as_view(), name='home'),
	path('requests/', PaymentDoneView.as_view(), name='paymentdone_requests'),
	
	path('user/<int:username>/', UserView.as_view(), name='user'),
]

