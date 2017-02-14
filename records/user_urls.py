from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import TemplateView


from django.contrib.auth.decorators import user_passes_test, login_required, permission_required


import user_view 

urlpatterns = [

	#User Permissions related
	url(r'^listall$', user_view.listall, name='listuser'),
	url(r'^adduser$', user_view.adduser, name='adduser'),
	url(r'^edituser/(?P<user_id>\d+)$', user_view.edituser, name='edituser'),


	url(r'^deletepem/(?P<user_id>\d+)/(?P<pem_name>\w+)$', user_view.deletepem, name='deletepem'),
	url(r'^addpem/(?P<user_id>\d+)/(?P<pem_name>\w+)$', user_view.addpem, name='addpem'),
	

	]
