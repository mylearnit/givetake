from django.urls import include, path

from .views import Home, UserView, PaymentDoneView, SearchView
app_name='adminapp'

urlpatterns = [
	path('tree/', Home.as_view(), name='home'),
	path('requests/', PaymentDoneView.as_view(), name='paymentdone_requests'),
	
	path('user/<int:username>/', UserView.as_view(), name='user'),
	path('search/', SearchView.as_view(), name='search'),
	
]

