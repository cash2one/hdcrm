#coding: utf-8
from django.db import models
from django.contrib.auth.models import User

# User Permission 

PEMS_LIBS= {
	'MANAGER': u'总经理',
	'ADD_USR': u'添加用户',
	'ADD_CLIENT': u'添加客户',
	'VIEW_CLIENT': u'查看客户',
	'ADD_PRODUCT': u'添加产品',
	'ADD_ORDER': u'添加生产订单',
}

class UserPerm(models.Model):
	user = models.ForeignKey(User)
	perm = models.CharField(max_length=50, default='')
	created_date = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return "%s - %s" % (self.user, self.perm)

def can_add_user(self):
	return self.is_superuser or self.userperm_set.filter(perm='ADD_USR').exists()

def can_add_client(self):
	return self.is_superuser or self.userperm_set.filter(perm='ADD_CLIENT').exists()

def can_add_product(self):
	return self.is_superuser or self.userperm_set.filter(perm='ADD_PRODUCT').exists()

def can_add_order(self):
	return self.is_superuser or self.userperm_set.filter(perm='ADD_ORDER').exists()

def can_view_client(self):
	return self.is_superuser or self.userperm_set.filter(perm__in=['VIEW_CLIENT', 'ADD_CLIENT']).exists()

def ismanager(self):
	return self.is_superuser or self.userperm_set.filter(perm='MANAGER').exists()

def name(self):
	if len(self.first_name) > 0:
		return self.first_name
	else:
		return self.username

User.add_to_class('name', name)
User.add_to_class('adduser', can_add_user)
User.add_to_class('addclient', can_add_client)
User.add_to_class('addproduct', can_add_product)
User.add_to_class('addorder', can_add_order)
User.add_to_class('viewclient', can_view_client)
User.add_to_class('ismanager', ismanager)
