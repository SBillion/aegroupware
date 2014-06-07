# -*-coding:utf-8 -*
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

def login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		user = auth.authenticate(username=username, password=password)
		if user is not None and user.is_active:
			auth.login(request, user)
			#~ return HttpResponseRedirect(request.GET.get('next'))
			nextPage = request.GET.get('next')
			if nextPage is not None:
				return HttpResponseRedirect(nextPage)
			else:
				return HttpResponseRedirect("/portal/progress/")
		else:
			messages.add_message(request, messages.INFO, 'L\'identifiant ou le mot de passe que vous avez entré est incorrect !')
			return render_to_response('account/login.html',
			   context_instance=RequestContext(request))
	else:
		return render_to_response('account/login.html',
		   context_instance=RequestContext(request))

def register(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			return HttpResponseRedirect("/portal/progress/")
	else:
		form = UserCreationForm()
	return render_to_response("account/register.html", {'form': form, },
	   context_instance=RequestContext(request))

@login_required
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/account/login/")
