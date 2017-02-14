from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import TemplateView


from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

import client_view 

urlpatterns = [

	#Sell Add Client 
	url(r'^addclient$', client_view.addclient, name='addclient'),
	url(r'^myclient$', client_view.listclient, name='listclient'),
	url(r'^editclient/(?P<client_id>\d+)$', client_view.editclient, name='editclient'),
	url(r'^viewclient/(?P<client_id>\d+)$', client_view.viewclient, name='viewclient'),

	url(r'addlog/(?P<client_id>\d+)$', client_view.addlog, name='addclientlog'),
	url(r'viewlogs/(?P<client_id>\d+)$', client_view.viewlogs, name='viewclientlog'),
	
	]
