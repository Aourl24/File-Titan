from .models import File, Folder,Profile
from django import forms
from django.contrib.auth.models import User

class FileForm(forms.ModelForm):
	class Meta:
		model=File
		fields=['file']
		widgets={'file':forms.ClearableFileInput(attrs={'multiple':True,'id':'fle'})}


class FolderForm(forms.ModelForm):
	class Meta:
		model=Folder
		fields=['name','privacy']
		widgets={'name':forms.TextInput(attrs={'class':'input'}),'privacy':forms.TextInput(attrs={'class':'input'})}
		#widgets={'password':forms.TextInput(attrs={'id':'password','class':'hide','type':'password'})}

class FolderFormAlt(forms.ModelForm):
	class Meta:
		model=Folder
		fields=['name']


class EditUser(forms.ModelForm):
	class Meta:
		model=Profile
		fields=['bio','profile_photo']
		widgets={'bio':forms.TextInput(attrs={'class':'input'})}

