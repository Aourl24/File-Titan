from .models import File, Folder,Profile
from django import forms
from django.contrib.auth.models import User

class FileForm(forms.ModelForm):
	class Meta:
		model=File
		fields=['file']
		widgets={'file':forms.ClearableFileInput(attrs={'multiple':False,'id':'fle','class':'form-control'})}


class FolderForm(forms.ModelForm):
	class Meta:
		model=Folder
		fields=['name']
		widgets={'name':forms.TextInput(attrs={'class':'form-control'}),'privacy':forms.Select(attrs={'class':'input'})}
		#widgets={'password':forms.TextInput(attrs={'id':'password','class':'hide','type':'password'})}

class EditFolder(forms.ModelForm):
	class Meta:
		model=Folder
		fields =['name']
		widgets={'name':forms.TextInput(attrs={'class':'form-control'})}

class FolderFormAlt(forms.ModelForm):
	class Meta:
		model=Folder
		fields=['name']


class EditUser(forms.ModelForm):
	class Meta:
		model=Profile
		fields=['bio','profile_photo']
		widgets={'bio':forms.Textarea(attrs={'class':'form-control'})}

