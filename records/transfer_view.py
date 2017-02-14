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
from records.order_model import Order, OrderItem, OrderItemForm
from records.transfer_model import OrderCashFlow, IncomeForm, ExpenseForm


def addOrderIncome(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	if request.method == 'POST':
		form = IncomeForm(request.POST)
		if form.is_valid():
			income = form.save(commit=False)
			income.order = order
			income.user = request.user
			income.save()

			messages.add_message(request, messages.SUCCESS, u'成功添加收入 %s' % income.amount)
			return HttpResponseRedirect(reverse('vieworder', 
				kwargs={'order_id': order.id }))
	else:
		form = IncomeForm()
	return render(request, 'transfer/addorderincome.html', 
		{'order': order, 'form': form})


def addOrderExpense(request, order_id):
	order = get_object_or_404(Order, pk=order_id)
	order = get_object_or_404(Order, pk=order_id)
	if request.method == 'POST':
		form = ExpenseForm(request.POST)
		if form.is_valid():
			income = form.save(commit=False)
			income.amount = income.amount*-1
			income.order = order
			income.user = request.user
			income.save()

			messages.add_message(request, messages.SUCCESS, u'成功添加支出 %s' % income.amount)
			return HttpResponseRedirect(reverse('vieworder', 
				kwargs={'order_id': order.id }))
	else:
		form = ExpenseForm()
	return render(request, 'transfer/addorderexpense.html', 
		{'order': order, 'form': form})


def deleteTransfer(request, transfer_id):
	cashFlow = get_object_or_404(OrderCashFlow, pk=transfer_id)

	cashFlow.delete()

	return HttpResponse(u'成功删除')


