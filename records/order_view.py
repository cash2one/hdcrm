#coding: utf-8

from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django import forms
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.decorators import user_passes_test, login_required, permission_required
from django.forms.models import model_to_dict
from records.order_model import Order, PackingForm, OrderItem, OrderItemForm
from records.order_model import OrderAccount, OrderAccountForm
from records.order_model import OrderDeliver, OrderDeliverForm
from records.client_model import Client

@login_required
def myorders(request):
	orders = request.user.order_set.all()
	return render(request, 'order/myorders.html', {'orders': orders})

@login_required
def addorder(request, client_id):
	client = get_object_or_404(Client, pk=client_id)

	order = client.order_set.create(user=request.user)

	return HttpResponseRedirect(reverse('vieworder', 
 			kwargs={'order_id': order.pk})) 


@login_required
def vieworder(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	additemform =  OrderItemForm()
	additemform.setorder(order)
	return render(request, 'order/vieworder.html', {'order': order, 'additemform': additemform})


@login_required
def printOrder(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	return render(request, 'order/printorder.html', {'order': order})


from django.forms import inlineformset_factory

import pdb
@login_required
def additem(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	if request.method == 'POST':
		form = OrderItemForm(request.POST)
		if form.is_valid():
			orderitem = form.save(commit=False)
			orderitem.order=order
			orderitem.save()
			messages.add_message(request, 
				messages.SUCCESS, 
				u'添加产品 %s 成功' % orderitem.product.name)
		else:
			messages.add_message(request, 
				messages.ERROR, 
				u'添加产品 错误')
		return HttpResponseRedirect(reverse('vieworder', 
 			kwargs={'order_id': order.pk})) 
	return HttpResponse("Error")
		
@login_required
def addorderaccount(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	if request.method == 'POST':
		form = OrderAccountForm(request.POST)
		if form.is_valid():
			oa = form.save(commit=False)
			oa.order=order
			oa.save()
			messages.add_message(request, 
				messages.SUCCESS, 
				u'修改财务信息成功')
			return HttpResponseRedirect(reverse('vieworder', 
 			kwargs={'order_id': order.pk})) 
		else:
			messages.add_message(request, 
				messages.ERROR, 
				u'修改财务信息错误')
	else:
		if order.orderaccount_set.all().exists():
			form = OrderAccountForm(instance=order.orderaccount_set.first())
		else:
			form=OrderAccountForm()
		form.fields['paymentterm'].initial = order.client.paymentterm
	
	return render(request, 'order/addorderaccount.html',
	 {'order': order, 'form': form})
	
@login_required
def adddeliver(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	if request.method == 'POST':
		form = OrderDeliverForm(request.POST)
		if form.is_valid():
			oa = form.save(commit=False)
			oa.order=order
			oa.save()
			messages.add_message(request, 
				messages.SUCCESS, 
				u'修改交货期成功')
			return HttpResponseRedirect(reverse('vieworder', 
 			kwargs={'order_id': order.pk})) 
		else:
			messages.add_message(request, 
				messages.ERROR, 
				u'修改交货期错误')
	else:
		if order.orderDeliver() is not None:
			form = OrderDeliverForm(instance=order.orderDeliver())
		else:
			form=OrderDeliverForm()
		
	return render(request, 'order/adddeliver.html',
	 {'order': order, 'form': form})
	

def changestatus(request, order_id, new_status):
	# PENDING, ACTIVE, DONE
	order = get_object_or_404(Order, pk=order_id)

	if new_status == 'SUBMIT':
		# Validate 
		if order.orderitem_set.filter(status=True).exists() is False:
			messages.add_message(request, 
				messages.ERROR, 
				u'！！！！ 提交失败！！！ 订单里没有产品，请添加')
		elif order.orderaccount_set.all().exists() is False:
			messages.add_message(request, 
				messages.ERROR, 
				u'！！！！ 提交失败！！！ 请填写财务信息')
		elif order.orderdeliver_set.all().exists() is False:
			messages.add_message(request, 
				messages.ERROR, 
				u'！！！！ 提交失败！！！ 请填写交货信息')
		elif len(order.packing) is 0:
			messages.add_message(request, 
				messages.ERROR, 
				u'！！！！ 提交失败！！！ 请填写组装或包装信息')
		else:
			order.status = new_status
			order.save()
	else:
		order.status = new_status
		order.save()
	return HttpResponseRedirect(reverse('vieworder', 
 			kwargs={'order_id': order.pk})) 

def disableorderitem(request, item_id):
	orderitem = get_object_or_404(OrderItem,pk=item_id)
	orderitem.status=False
	orderitem.save()
	return HttpResponseRedirect(reverse('vieworder', 
 			kwargs={'order_id': orderitem.order.pk}))



def editorderpacking(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	if request.method == 'POST':
		form = PackingForm(request.POST)
		if form.is_valid():
			order.packing = form.cleaned_data['packing']
			order.save()
			messages.add_message(request, 
				messages.SUCCESS, 
				u'修改组装包装 成功')
			return HttpResponseRedirect(reverse('vieworder', 
 			kwargs={'order_id': order.pk})) 
		else:
			messages.add_message(request, 
				messages.ERROR, 
				u'修改组装包装  错误')
	else:
		form=PackingForm()
		form.fields['packing'].initial=order.packing
		
	return render(request, 'order/editorderpacking.html',
	 {'order': order, 'form': form})
	
