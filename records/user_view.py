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
from django.forms import ModelForm
from records.user_model import PEMS_LIBS
from user_model import UserPerm



class AddUserForm(forms.Form):
	username = forms.CharField(max_length=20, label=u'用户名')
	password = forms.CharField(max_length=50, label='Password')
	
	def clean_username(self):
		username = self.cleaned_data['username']
		if User.objects.filter(username=username).exists():
			raise ValidationError('"%s" User exists' % username)
		return username


@login_required
def adduser(request):
	if request.user.adduser() is False:
		return HttpResponse(u"你没有权限")

	if request.method == 'POST':
		form = AddUserForm(request.POST)
		if form.is_valid():
			# add user 
			user = User.objects.create_user(form.cleaned_data['username'], '', form.cleaned_data['password'])
			messages.add_message(request, messages.SUCCESS, 'User("%s") added success!' % user.username)
			return HttpResponseRedirect(reverse('listuser'))
	else:
		form = AddUserForm()

	return render(request, 'adduser.html', {'form': form})

class EditUserForm(forms.Form):
	name = forms.CharField(max_length=20, label=u'名字')
	password = forms.CharField(max_length=50, label=u'新的密码')
	
	def clean_password(self):
		password = self.cleaned_data['password']
		if len(password) is 0:
			raise ValidationError('Password cannot be empty')
		return password

import pdb

@login_required
def edituser(request, user_id):
	if request.user.adduser() is False and request.user.pk is not int(user_id):
		return HttpResponse(u"你没有权限")

	user = get_object_or_404(User, pk=user_id)
	if request.method == 'POST':
		form = EditUserForm(request.POST)
		
		if form.is_valid():
			# add user 
			user.first_name=form.cleaned_data['name']
			user.set_password(form.cleaned_data['password'])
			user.save()
			messages.add_message(request, messages.SUCCESS, 'User("%s") updated success!' % user.username)
			return HttpResponseRedirect(reverse('userhome'))
	else:
		form = EditUserForm()
		form.fields['name'].initial = user.first_name

	return render(request, 'edituser.html', {'form': form, 'user': user})


def listall(request):
	if request.user.adduser() is False:
		return HttpResponse(u"你没有权限")

	permname = []
	permdisp = []
	for pem in PEMS_LIBS:
		permname.append(pem)
		# print(pem)
		# print(PEMS_LIBS[pem])
		permdisp.append(PEMS_LIBS[pem])
	
	users = User.objects.all()

	userlist = []
	for user in users:
		obj = {'user': user, 'perms':[]}
		for pem in permname:
			if UserPerm.objects.filter(user=user, perm=pem).exists():
				obj['perms'].append({'status': True, 
					'disp':PEMS_LIBS[pem],
					'name':pem})
			else:
				obj['perms'].append({'status': False, 
					'disp':PEMS_LIBS[pem],
					'name':pem })
		userlist.append(obj)


	return render(request, 'userlist.html',
	 {'pemname': permname, 'permdisp': permdisp, 'userlist': userlist})


def deletepem(request, user_id, pem_name):
	if request.user.adduser() is False:
		return HttpResponse(u"你没有权限")

	user = User.objects.get(pk=user_id)
	user.userperm_set.filter(perm=pem_name).delete()
	return redirect(reverse('listuser' ))

def addpem(request,user_id, pem_name):
	if request.user.adduser() is False:
		return HttpResponse(u"你没有权限")

	user = User.objects.get(pk=user_id)
	user.userperm_set.create(perm=pem_name)
	return redirect(reverse('listuser' ))
	


