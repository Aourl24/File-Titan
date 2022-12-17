from django.db import models
from django.urls import reverse
from FileShare.settings import BASE_DIR
from django.http import StreamingHttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from datetime import datetime

class Profile(models.Model):
    user=models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE)
    date_joined=models.DateTimeField(auto_now_add=True, blank=True, null=True)
    bio=models.CharField('About', max_length=100, blank=True, null=True)
    location=models.CharField(max_length=100, blank=True, null=True)
    profile_photo=models.ImageField(upload_to='profileimage', default='media/profile.png', null=True, blank=True)
    mode=models.CharField(max_length=100, default='white')
    
    def __str__(self):
        return self.user.username
        
    def get_absolute_url(self):
        return reverse('ProfileUrl', args=[self.id])

class Folder(models.Model):
	owner=models.ForeignKey(Profile, related_name='folder', null=True, blank=True, on_delete=models.CASCADE)
	profiles=models.ManyToManyField(Profile, blank=True, related_name='our_folder')
	name=models.CharField(max_length=10000)
	local_path=models.CharField(max_length=10000,default='C:/Users/USER/Documents/WDP/Django/',null=True,blank=True)
	parent=models.ForeignKey('self',related_name='child_folder',blank=True,null=True, on_delete=models.CASCADE)
	privacy=models.CharField(choices=[('public', 'public'), ('private', 'private'), ('authorize', 'authorize')], default='public', max_length=20)
	password=models.CharField(max_length=20, blank=True, null=True)
	date_created=models.DateTimeField(auto_now_add=True)
	last_updated=models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('FolderDetailViewUrl',args=[self.id])

	def Delete(self):
		Folder.objects.get(id=self.id).delete();
		return reverse('FileViewUrl')

	def download(self):
		k=Folder.objects.get(id=self.id).file.all()
		for i in k:
			yield i.file
		

	

class File(models.Model):
	folder=models.ForeignKey(Folder,related_name='file', on_delete=models.CASCADE,null=True,blank=True)
	name=models.CharField(max_length=10000)
	file=models.FileField(upload_to='file',default='file/empty.txt')
	edited=models.ForeignKey('self',related_name='edited_file',blank=True,null=True,on_delete=models.CASCADE)
	edit_owner=models.ForeignKey(Profile,null=True,blank=True,related_name='my_file_edit',on_delete=models.CASCADE)
	date_created=models.DateTimeField(auto_now_add=True)
	last_updated=models.DateTimeField(auto_now=True)
	clone=models.BooleanField(default=False)
    
	def __str__(self):
		return self.name

	def Delete(self):
		File.objects.get(id=self.id).delete()
		return reverse('FileViewUrl')
		

	def openFile(self):
		f_name=str(BASE_DIR.joinpath(self.file.url[1:]))
		with open(f_name,'r') as obj:
			a=obj.read()
			

		return str(a)

	def branch(self):
		return reverse('BranchUrl',args=[self.id])

	def saveFile(self,words):
		f_name=str(BASE_DIR.joinpath(self.file.url[1:]))
		with open(f_name,'w') as obj:
			obj.write(words)
		
		return

	def saveLocally(self,words,path=None):
		if self.folder:
			f_nam=str(self.folder.local_path)
		else:
			f_nam=path
		f_name=str(BASE_DIR.joinpath(f_nam  +'/' + self.name))
		with open(f_name,'w') as obj:
			obj.write(words)
		
		return


	def get_absolute_url(self):
		return reverse('FileDetailViewUrl',args=[self.id])
		
	def createBranch(self,owner):
		b=File.objects.get(id=self.id)
		u=b.folder
		word=b.openFile()
		con=ContentFile(word, f'branch_{self.name}')
		j=File.objects.create(name=self.name,folder=self.folder,file=con,edited=b,edit_owner=owner)
		return reverse('BranchUrl',args=[self.id])
		
	def clone(self,owner,folder):
		b=File.objects.get(id=self.id)
		u=b.folder
		j=File.objects.create(name=self.name,folder=folder,file=self.file, clone=True)
		#return reverse('BranchUrl',args=[self.id])

	def replace(self,x):
		#b=File.objects.get(id=self.id)
		m=File.objects.get(id=x)
		word=m.openFile()
		self.saveFile(word)
		return

	def merge(self,x):
		#b=File.objects.get(id=self.id)
		m=File.objects.get(id=x)
		d=self.openFile()
		k=m.openFile()
		l=d.split('\n') + k.split('\n')
		e=sorted(set(l),key=l.index)
		v=('\n').join(e)

		self.saveFile(v)
		return

#ContentFile('',name=f'{b}'),

@receiver(post_save, sender=User)
def ProfileCreated(sender, created, instance,**kwargs):
    if created:
        Profile.objects.create(user=instance)

# @reciver(post_save,sender=File)
# def OwnerFile(sender,created,instance,**kwargs):
# 	if created:
# 		instance.owner = instance.folder.owner