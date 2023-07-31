from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect,reverse
#from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .models import Folder,Profile

def CheckAccess(func):
	def wrap(request, *args, **kwargs):

		if 'fid' in kwargs.keys():
			b=Folder.objects.get(id=kwargs['fid'])

			if request.user.is_authenticated:
				if b.owner == Profile.objects.get(user=request.user):
					return func(request, *args, **kwargs)

			if b.privacy == 'authorize':
				try:
					check=request.session[f"folder{kwargs['fid']}"]
					
				except KeyError:
					check='notallow'
					request.session[f"folder{kwargs['fid']}"]= 'notallow'

				print(check)
				if  check == 'allow' :
					pass

				else:
					return redirect('GiveAcessUrl',id=kwargs['fid'])

		return func(request,*args,**kwargs)


	return wrap

def Confirmation(func):
	def wrap(request,*args,**kwargs):

		pass
	pass

# def checkPrivate(func):
# 	def wrap(request,*args,**kwargs):
# 		if request.method == 'POST':
# 		c=request.POST['privacy']
# 		if c:
# 			d=request.POST.get('password')