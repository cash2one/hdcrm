from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import TemplateView


from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

import order_view 

urlpatterns = [

	url(r'^myorders$', order_view.myorders, name='myorders'),
	
	url(r'^addorder/(?P<client_id>\d+)$', order_view.addorder, name='addorder'),

	url(r'^vieworder/(?P<order_id>\d+)$', order_view.vieworder, name='vieworder'),
	
	url(r'^printorder/(?P<order_id>\d+)$', order_view.printOrder, name='printOrder'),

	url(r'^additem/(?P<order_id>\d+)$', order_view.additem, name='additem'),

	url(r'^addorderaccount/(?P<order_id>\d+)$', order_view.addorderaccount, name='addorderaccount'),
	url(r'^adddeliver/(?P<order_id>\d+)$', order_view.adddeliver, name='adddeliver'),


	url(r'^changestatus/(?P<order_id>\d+)/(?P<new_status>\w+)$', order_view.changestatus, name='changeorderstatus'),

	url(r'^editorderpacking/(?P<order_id>\d+)$', order_view.editorderpacking, name='editorderpacking'),

	url(r'^disableorderitem/(?P<item_id>\d+)$', order_view.disableorderitem, name='disableorderitem'),

	#Sell Add product from client

	# url(r'^addproduct/(?P<client_id>\d+)$', product_view.addproduct, name='addproduct'),
	# url(r'^editproduct/(?P<product_id>\d+)$', product_view.editproduct, name='editproduct'),

	# url(r'^viewprod/(?P<product_id>\d+)$', product_view.viewproduct, name='viewproduct'),

	]
