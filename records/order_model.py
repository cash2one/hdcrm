#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from records.client_model import Client
from records.product_model import Product
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from django import forms

# User Permission 

ORDER_STATUS_CHOICE=(
	('PENDING', u'草稿'),
	('SUBMIT', u'提交'),
	('DONE', u'发货'),
	)

class Order(models.Model):
	user = models.ForeignKey(User)
	client= models.ForeignKey(Client)

	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now = True)

	packing = models.TextField(blank=True)

	# PENDING, 
	status = models.CharField(max_length=20, 
		choices=ORDER_STATUS_CHOICE,
		default='PENDING')
	
	def canedit(self):
		return self.status=='PENDING'

	def accountInfo(self):
		try:
			return self.orderaccount_set.first()
		except OrderAccount.DoesNotExist:
			return None
	def orderDeliver(self):
		try:
			return self.orderdeliver_set.first()
		except OrderDeliver.DoesNotExist:
			return None

	class Meta:
		ordering = ["-created_date"]

class PackingForm(ModelForm):
	class Meta:
		model = Order
		fields=('packing',)


ACCOUNT_CHOICE = (
	('CON_US', u'建行-美金'),
	('CON_RMB', u'建行-人民币'),
	('WESTUNION', u'西联'),
	('ALIBABA_US', u'阿里巴巴-美金'),
	('ALIBABA_RMB', u'阿里巴巴-人民币'),
	('PAYPAL1',u'贝宝-lianhuness@gmail.com'),
	('PAYPAL2', u'贝宝-yiqizhu@hongdalatex.com'),
	('ZENRONGMEI',u'曾-农行'),
	)

class OrderAccount(models.Model):
	order = models.ForeignKey(Order)
	created_date = models.DateTimeField(auto_now_add=True)
	account = models.CharField(max_length=20, 
		choices=ACCOUNT_CHOICE)
	
	total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
	paymentterm = models.CharField(max_length=200,default=u'款到发货')

	def __unicode__(self):
		return "%s %s"%(self.get_account_display(), self.total)
	
	class Meta:
		ordering = ["-created_date"]

class OrderAccountForm(ModelForm):
	class Meta:
		model = OrderAccount
		fields = ('account', 'total', 'paymentterm')
		# widgets = {'order': forms.HiddenInput()}

class OrderDeliver(models.Model):
	order = models.ForeignKey(Order)
	created_date = models.DateTimeField(auto_now_add=True)
	deliverDate = models.DateField()

	class Meta:
		ordering=['-created_date']

	def __unicode__(self):
		return self.deliverDate.strftime('%Y-%m-%d')

class OrderDeliverForm(ModelForm):
	class Meta:
		model = OrderDeliver
		fields = ('deliverDate',)

class OrderItem(models.Model):
	order = models.ForeignKey(Order)
	created_date=models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now = True)
	
	product = models.ForeignKey(Product)
	product_snap = models.TextField(default='')  # Used for tempory product display 
	amount = models.PositiveIntegerField()
	note = models.TextField(blank=True)
	status = models.BooleanField(default=True)

	def __unicode__(self):
		return "%s - %s" %(self.product.name, self.amount)
	class Meta:
		ordering = ["created_date"]


@receiver(pre_save, sender=OrderItem)
def orderitem_log_message(sender,instance, using, **kwargs):
	product = instance.product
	msg = u'%s-%s(%s)\n  颜色 %s-%s\n 说明:%s'%(product.get_group_display(), 
	 product.name,
	 product.size,
	 product.color,
	 product.phantom,
	 product.info)
	print(msg)
	instance.product_snap = msg


import pdb

class OrderItemForm(ModelForm):
	class Meta:
		model = OrderItem
		fields = ('product', 'amount', 'note')
		# widgets = {'order': forms.HiddenInput()}

	def __init__(self,  *args, **kwargs):
		super(OrderItemForm, self).__init__(*args, **kwargs)
	
	def setorder(self, order):
		self.fields['product'].queryset = Product.objects.filter(client=order.client)
		# self.fields['order'].initial = order

