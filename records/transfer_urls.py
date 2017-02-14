from django.conf.urls import url
from django.conf.urls import url, include
from django.views.generic import TemplateView


from django.contrib.auth.decorators import user_passes_test, login_required, permission_required

import transfer_view 

urlpatterns = [

	# url(r'^myorders$', order_view.myorders, name='myorders'),
	
	url(r'^addorderincome/(?P<order_id>\d+)$', 
		transfer_view.addOrderIncome, 
		name='addorderincome'),

	url(r'^addorderexpense/(?P<order_id>\d+)$', 
		transfer_view.addOrderExpense, 
		name='addorderexpense'),

	url(r'^delete/(?P<transfer_id>\d+)$',
		transfer_view.deleteTransfer,
		name='deleteTransfer'),
	
	# url(r'^additem/(?P<order_id>\d+)$', order_view.additem, name='additem'),

	# url(r'^addorderaccount/(?P<order_id>\d+)$', order_view.addorderaccount, name='addorderaccount'),
	# url(r'^adddeliver/(?P<order_id>\d+)$', order_view.adddeliver, name='adddeliver'),


	# url(r'^changestatus/(?P<order_id>\d+)/(?P<new_status>\w+)$', order_view.changestatus, name='changeorderstatus'),

	# url(r'^disableorderitem/(?P<item_id>\d+)$', order_view.disableorderitem, name='disableorderitem'),

	

	]
