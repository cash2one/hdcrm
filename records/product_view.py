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
from records.product_model import Product, ProductForm, ProductFile, ProductFileForm
from records.client_model import Client

@login_required
def listproduct(request):
	products = Product.objects.all()
	return render(request, 'product/listproducts.html', {'products': products})

@login_required
def addproduct(request, client_id):
	client = get_object_or_404(Client, pk=client_id)

	if request.user.addproduct() is False:
		return HttpResponse(u"你没有权限")

	if request.method == 'POST':
		form = ProductForm(request.POST)
		if form.is_valid():
			product = form.save(commit=False)
			product.user = request.user
			product.client=client
			product.save()
			messages.add_message(request, messages.SUCCESS, u'成功添加新客人 %s' % product.name)
			return HttpResponseRedirect(reverse('viewclient', 
				kwargs={'client_id': client.id }
				))
	else:
		form = ProductForm()
	return render(request, 'product/addproduct.html', {'form': form, 'client': client})

@login_required
def editproduct(request, product_id):
	if request.user.addproduct() is False:
		return HttpResponse(u"你没有权限")

	product = get_object_or_404(Product, pk=product_id)
	if request.method == 'POST':
		product = ProductForm(request.POST, instance=product).save()
		messages.add_message(request, messages.SUCCESS, 'Product ("%s") updated success!' % product.name)
		return HttpResponseRedirect(reverse('viewclient', 
			kwargs={'client_id': product.client.pk}))
	else:
		form = ProductForm(instance=product)
	return render(request, 'product/editproduct.html', {'form': form, 'product': product})

@login_required
def viewproduct(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	return render(request, 'product/viewproduct.html', {'product': product})

@login_required
def productuploadfile(request, product_id):
	product = get_object_or_404(Product, pk=product_id)
	
	if request.method == 'POST':
		form = ProductFileForm(request.POST, request.FILES)
		if form.is_valid():
			c = form.save(commit=False)
			c.user = request.user
			c.product = product
			c.save()

			messages.add_message(request, messages.SUCCESS, 
			 u'文件添加成功! %s'%c.filename)

			return HttpResponseRedirect(reverse('viewproduct', 
 			kwargs={'product_id': product.pk})) 
	else:
		form = ProductFileForm()
	return render(request, 'product/uploadfile.html', {'form': form, 'product': product})


@login_required
def deletefile(request, productfile_id):
	pf = get_object_or_404(ProductFile, pk=productfile_id)
	pf.delete()
	messages.add_message(request, messages.SUCCESS, 
			 u'文件删除成功! %s'%pf.filename)
	return HttpResponseRedirect(reverse('viewproduct', 
 			kwargs={'product_id': pf.product.pk})) 

