#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from records.client_model import Client
from records.product_model import Product
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django import forms
from records.order_model import Order, ACCOUNT_CHOICE
# User Permission 

CURRENCY_CHOICE = (
	('USD', u'美金'),
	('RMB', u'人民币')
	)

class OrderCashFlow(models.Model):
	order = models.ForeignKey(Order)
	user = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	
	date = models.DateField()
	currency = models.CharField(max_length=10, 
		choices=CURRENCY_CHOICE,
		default='RMB')
	
	account = models.CharField(max_length=20,
		choices=ACCOUNT_CHOICE,
		default='CON_RMB')

	amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	note = models.TextField()

	payto = models.CharField(max_length=100, blank=True)

	class Meta:
		ordering=['-date']

from datetime import datetime

class IncomeForm(ModelForm):
	class Meta:
		model = OrderCashFlow
		fields = ('date', 'currency', 'account', 'amount', 'note')
	def __init__(self,  *args, **kwargs):
		super(IncomeForm, self).__init__(*args, **kwargs)
		self.fields['date'].initial = datetime.today()
	
class ExpenseForm(ModelForm):
	class Meta:
		model = OrderCashFlow
		fields = ('date', 'amount', 'payto', 'note')
	def __init__(self,  *args, **kwargs):
		super(ExpenseForm, self).__init__(*args, **kwargs)
		self.fields['date'].initial = datetime.today()
	
