from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import TemplateView


from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

import product_view 

urlpatterns = [

	url(r'^productlist$', product_view.listproduct, name='listproduct'),
	
	#Sell Add product from client

	url(r'^addproduct/(?P<client_id>\d+)$', product_view.addproduct, name='addproduct'),
	url(r'^editproduct/(?P<product_id>\d+)$', product_view.editproduct, name='editproduct'),

	url(r'^viewprod/(?P<product_id>\d+)$', product_view.viewproduct, name='viewproduct'),

	url(r'^uploadfile/(?P<product_id>\d+)$', product_view.productuploadfile, name='productuploadfile'),
	url(r'^deletefile/(?P<productfile_id>\d+)$', product_view.deletefile, name='deleteproductfile'),
	]
