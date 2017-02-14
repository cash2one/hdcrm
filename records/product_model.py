#coding: utf-8
from django.db import models
from django.contrib.auth.models import User
from django.forms import ModelForm
from records.client_model import Client
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save

# User Permission 

PRODUCT_CHOICES=(
	('41LOOP', u'208厚圈'),
	('LOOP', u'小胶圈'),
	('YOGABAND', u'拉力带'),
	('DANGONG', u'弹弓片'),
	('PVC', u'PVC产品'),
	('OLD', u'老产品'),
	('TRADING', u'外协外购'),
	)

class Product(models.Model):
	user = models.ForeignKey(User)
	client= models.ForeignKey(Client)

	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now = True)

	name = models.CharField(max_length=200)
	group = models.CharField(max_length=15,
		choices=PRODUCT_CHOICES)
	size = models.CharField(max_length=100, default='NA')
	color = models.CharField(max_length=100, default='NA')
	phantom = models.CharField(max_length=100, default='NA')
	material = models.CharField(max_length=100, default='NA')
	info = models.TextField()

	quote = models.DecimalField(max_digits=5, decimal_places=2, default=0)

	def gracedisplay(self):
		return "%s-%s-%s-%s-%s-%s-%s"%(self.name, self.group, self.size, self.color, self.phantom, self.material, self.info)
	# HDP-5###
	def __unicode__(self):
		return "HDP%s-%s"%(self.pk, self.name )

class ProductLog(models.Model):
	created_date = models.DateTimeField(auto_now_add=True)
	product = models.ForeignKey(Product)
	message = models.CharField(max_length=200)

	def __unicode__(self):
		return self.message

	class Mega:
		ordering = ['-created_date']

def user_directory_path(instance, filename):
	# temp = get_random_string(length=10)
	return 'uploads/product/%s/%s%s'%(instance.product.pk, instance.pk, filename)

import os 
class ProductFile(models.Model):
	product = models.ForeignKey(Product)
	user = models.ForeignKey(User)
	created_date = models.DateTimeField(auto_now_add=True)
	filename = models.CharField(max_length=100)
	upload = models.FileField(upload_to=user_directory_path)

	def isImage(self):
		filename, file_extension = os.path.splitext(self.upload.url)
		return file_extension.lower() in ['.jpeg', '.jpg', '.png']

class ProductFileForm(ModelForm):
	class Meta:
		model = ProductFile
		fields = ['filename', 'upload']
		labels = {'filename': u'标题',
				'upload': u'选择附件'}

	# def clean_upload(self):
	# 	upload = self.cleaned_data.get('upload', False)
	# 	if upload:
	# 		print(upload._size)
	# 		if upload._size > 10*1024*1024:
	# 			raise ValidationError("File Size Too Big ")
	# 	else:
	# 		raise ValidationError("Couldnot read file")
	# 	return upload

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'group', 'size', 'color', 'phantom', 'material'
		, 'quote', 'info')
   



@receiver(post_save, sender=Product)
def product_log_message(sender,instance, created, using, **kwargs):
	msg = u'%s updated %s'%(instance.user.name(), instance.gracedisplay())
	print(msg)
	ProductLog.objects.create(product=instance, message=msg)

