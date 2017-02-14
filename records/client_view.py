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
from records.client_model import Client, ClientForm, ClientLog, ClientLogForm

@login_required
def addclient(request):
	if request.user.addclient() is False:
		return HttpResponse(u"你没有权限")

	if request.method == 'POST':
		form = ClientForm(request.POST)
		if form.is_valid():
			client = form.save(commit=False)
			client.user = request.user
			client.save()

			messages.add_message(request, messages.SUCCESS, u'成功添加新客人 %s' % client.name)
			return HttpResponseRedirect(reverse('listclient'))
	else:
		form = ClientForm()
	return render(request, 'client/addclient.html', {'form': form})


@login_required
def editclient(request, client_id):
	if request.user.addclient() is False:
		return HttpResponse(u"你没有权限")
	client = get_object_or_404(Client, pk=client_id)
	if request.method == 'POST':
		client = ClientForm(request.POST, instance=client).save()
		messages.add_message(request, messages.SUCCESS, 'Client ("%s") updated success!' % client.name)
		return HttpResponseRedirect(reverse('viewclient', 
			kwargs={'client_id': client.pk}))
	else:
		form = ClientForm(instance=client)
	return render(request, 'client/editclient.html', {'form': form, 'client': client})


@login_required
def listclient(request):
	if request.user.addclient() is False:
		return HttpResponse(u"你没有权限")

	if request.user.ismanager():
		clientlist = Client.objects.all()
	else:
		clientlist = request.user.client_set.all()

	return render(request, 'client/listclient.html',
	 {'clientlist': clientlist})

@login_required
def viewclient(request, client_id):
	if request.user.viewclient() is False:
		return HttpResponse(u"你没有权限")
	client = get_object_or_404(Client, pk=client_id)

	return render(request, 'client/viewclient.html', {'client': client})

import datetime

@login_required
def addlog(request, client_id):
	client = get_object_or_404(Client, pk=client_id)

	if request.method == 'POST':
		form = ClientLogForm(request.POST)
		if form.is_valid():
			log = form.save(commit=False)
			log.user = request.user
			log.client=client
			log.save()
			messages.add_message(request, messages.SUCCESS, u'添加成功 ')
			return HttpResponseRedirect(reverse('viewclientlog', kwargs={'client_id': client.id}))
	else:
		form = ClientLogForm()
		if client.clientlog_set.all().exists():
			form.fields['nextDate'].initial = client.clientlog_set.first().nextDate
		else:
			one_week = datetime.timedelta(days=7)
			form.fields['nextDate'].initial = datetime.date.today() + one_week

	return render(request, 'client/addlog.html', {'client': client, 'form': form})


@login_required
def viewlogs(request, client_id):
	client = get_object_or_404(Client, pk=client_id)
	return render(request, 'client/viewlogs.html', {'client': client})

