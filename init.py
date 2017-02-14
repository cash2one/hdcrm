#coding: utf-8

import django
from django.conf import settings
# from crmdemo import settings as mysettings
import pdb
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hongda.settings") 

django.setup()

from django.contrib.auth.models import User, Group, Permission
from django.contrib.contenttypes.models import ContentType

from records.client_model import Client

# Create super user yiqi 
if not User.objects.filter(username='yiqi').exists():
	yiqi = User.objects.create_superuser('yiqi', '', 'hongdalatex')

	print("## Creating YIQI as admin, and add as 'MANAGER' ")
else:
	print(" Admin 'YIQI' exists, skip creating" )


# Create Lisai 

# Delete existing lisai 
testname = 'lisai'
User.objects.filter(username=testname).delete()

lisai = User.objects.create_user(testname, '',testname)

# Lisai can add client/product/
lisai.userperm_set.create(perm='ADD_CLIENT')
lisai.userperm_set.create(perm='ADD_PRODUCT')
lisai.userperm_set.create(perm='ADD_ORDER')

# Lisai add client "Starwoodsport"
# name = models.CharField(max_length=200)
# 	contact = models.CharField(max_length=200)
# 	tel = models.CharField(max_length=100)
# 	location = models.CharField(max_length=100)
# 	info = models.TextField()

testclient = 'starwoodsport'

# Delete existing client 
Client.objects.filter(name=testclient).delete()
client = lisai.client_set.create(name=testclient, 
	contact='William', 
	tel='N/A',
	location='UK',
	info='Amazon Top Seller')

# Add product in the client 

# ('41LOOP', u'208厚圈'),
# 	('LOOP', u'小胶圈'),
# 	('YOGABAND', u'拉力带'),
# 	('DANGONG', u'弹弓片'),
# 	('PVC', u'PVC产品'),
# 	('OLD', u'老产品'),
# 	('TRADING', u'外协外购'),

names = [('POWERBAND-1.3-RED', '41LOOP', '208*1.3*0.45cm', 1.52, 'RED'),
		('POWERBAND-2.2-BLACK', '41LOOP', '208*2.2*0.45cm', 1.52, 'RED'),
		('POWERBAND-3.2-PURPLE', '41LOOP', '208*3.2*0.45cm', 1.52, 'RED'),
		('POWERBAND-4.4-GREEN', '41LOOP', '208*4.4*0.45cm', 1.52, 'RED'),
		('POWERBAND-6.3-BLUE', '41LOOP', '208*6.4*0.45cm', 1.52, 'RED'),
		(u'说明书-UK', 'TRADING', 'N/A', 1.52, 'N/A'),
		(u'说明书-US', 'TRADING', 'N/A', 1.52, 'N/A'),
		(u'说明书-德国', 'TRADING', 'N/A', 1.52, 'N/A'),
		
		(u'福建轮', 'TRADING', 'N/A', 1.52, 'N/A'),
]
# name = models.CharField(max_length=200)
# 	group = models.CharField(max_length=15,
# 		choices=PRODUCT_CHOICES)
# 	size = models.CharField(max_length=100, default='NA')
# 	color = models.CharField(max_length=100, default='NA')
# 	phantom = models.CharField(max_length=100, default='NA')
# 	material = models.CharField(max_length=100, default='NA')
# 	info = models.TextField()

# 	quote = models.DecimalField(max_digits=5, decimal_places=2, default=0)

for item in names:
	client.product_set.create(user=lisai, 
		name=item[0],
		group=item[1],
		size=item[2],
		color=item[4],
		phantom='N/A',
		material='N/A',
		info='N/A',
		quote=item[3])


