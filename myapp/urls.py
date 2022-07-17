from django.urls import include, path
from django.views.generic import TemplateView

from .views import Dashboard, GiveHelp, ReceiveHelp, ReceiveHelpChart
app_name='myapp'

urlpatterns = [
	path('dashboard/', Dashboard.as_view(), name='dashboard'),
	path('givehelp/', GiveHelp.as_view(), name='givehelp'),
	# admin view for a user
	# path('givehelp/<int:username>/', GiveHelp.as_view(), name='givehelp'),
	
	path('receivehelp/', ReceiveHelp.as_view(), name='receivehelp'),
	path('receivehelpchart/', ReceiveHelpChart.as_view(), name='receivehelpchart'),
	path('faq/', TemplateView.as_view(template_name="guest/faq.html"), name="faq"),
	path('legal/', TemplateView.as_view(template_name="guest/legal.html"), name="legal"),
	path('contact/', TemplateView.as_view(template_name="guest/contact.html"), name="contact"),
	path('tandc/', TemplateView.as_view(template_name="guest/tandc.html"), name="tandc"),
]
