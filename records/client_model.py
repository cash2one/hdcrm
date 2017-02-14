#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm

# User Permission 

CLIENT_RANKING_CHOICE = (
	('A', u'开发阶段'),
	('B', u'正常操作阶段'),
	('C', u'重点客户'),
	)

class Client(models.Model):
	user = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now = True)
	name = models.CharField(max_length=200)
	contact = models.CharField(max_length=200)
	ranking = models.CharField(max_length = 10, 
		choices=CLIENT_RANKING_CHOICE, default='A')
	tel = models.CharField(max_length=100)
	location = models.CharField(max_length=100)
	paymentterm = models.CharField(max_length=100, default=u'款到发货')
	info = models.TextField()

	# HDC###
	def __unicode__(self):
		return "HDC%s - %s"%(self.pk, self.name )

class ClientForm(ModelForm):
	class Meta:
		model = Client
		fields = ('name', 'ranking', 'contact', 'tel',  'location', 'paymentterm', 
			'info')
        labels = {
            'name': u'名称',
            'contact': u'联系人',
            'tel': u'电话',
            'location': u'地区',
            'info': u'补充信息',
        }
        help_texts = {
            'info': u'客源? 预期? 其他',
        }

import datetime

class ClientLog(models.Model):
	client=models.ForeignKey(Client)
	user = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	note = models.TextField()
	nextDate = models.DateField()

	class Meta:
		ordering = ["-created_date"]

	def needAction(self):
		return datetime.date.today() >= self.nextDate

class ClientLogForm(ModelForm):
	class Meta:
		model = ClientLog
		fields = ('note', 'nextDate')
	
