from django.db import models
from django.urls import reverse
from FileShare.settings import BASE_DIR
from django.http import StreamingHttpResponse,HttpResponse,FileResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from datetime import datetime
import zipfile

class Header(models.Model):
    title=models.CharField(max_length=1000)
    background_color=models.CharField(max_length=100,default='white')
        
    def __str__(self):
        return self.title
        
class SubHeader(models.Model):
    header=models.ForeignKey(Header,related_name='SubHeader',on_delete=models.CASCADE)
    title=models.CharField(max_length=10000)
    body=models.TextField()
    image=models.ImageField(blank=True,null=True,upload_to='subheader_images')
    
    def __str__(self):
        return self.title
        
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
	info=models.TextField('About Directory' ,null=True,blank=True)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse('FolderDetailViewUrl',args=[self.id])

	def Delete(self):
		Folder.objects.get(id=self.id).delete();
		return reverse('FileViewUrl')

	def createZip(self,z,folder,pa,folder_name):
		da=pa + '/' + folder_name + '/' 
		for j in folder.file.all():
			z.write(f'media/file/{j}',arcname=f'{da}/{j.folder}/{j}')
		f=Folder.objects.get(id=folder.id).child_folder.all()
		if f:
			for fold in f:
				#da+=folder.name + '/'
				self.createZip(z,fold,da,folder.name)
		
		return None

	def download(self):
		files=File.objects.filter(folder=self)
		files=self.file.all()
		k=Folder.objects.get(id=self.id).child_folder.all()
		n=Folder.objects.get(id=self.id).child_folder.all()
		q=[x.id for x in n]
		c=0
		pa=''
		path=str(BASE_DIR.joinpath(f'media/file/{self.name}.zip'))
		with zipfile.ZipFile(f'{path}',mode='w') as z:
			for i in files:
				p=str(BASE_DIR.joinpath())
				z.write(str(BASE_DIR.joinpath(f'media/{i.file}')),arcname=f'{i.folder}/{i}')

			pa=self.name + '/'
			m=list()
			done=list()
			if q:
				k=Folder.objects.get(id=q[c])
			else:
				k=False
			while k:
				for j in k.file.all():
					z.write(str(BASE_DIR.joinpath(f'media/{j.file}')),arcname=f'{self.name}/{j.folder}/{j}')
				v=Folder.objects.get(id=k.id).child_folder.all()

				if v:
					m.append(k.id)

				for no in m:

					Fold=Folder.objects.get(id=no).child_folder.all()

					for fod in Fold:
						self.createZip(z,fod,fod.parent.parent.name,fod.parent.name)


				if c == len(q):
					k=False
				else:
					k= Folder.objects.get(id=q[c])

					pa+=k.name + '/'
					c+=1

		return f'media/file/{self.name}.zip'
	

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
		#return reverse('FileViewUrl')
		

	def openFile(self):
		f_name=str(BASE_DIR.joinpath(self.file.url[1:]))
		with open(f_name,'r') as obj:
			a=obj.read()
			
		return str(a)

	def branch(self):
		return reverse('BranchUrl',args=[self.id])

	def saveFile(self,words):
		words=words.replace('”','"')
		f_name=str(BASE_DIR.joinpath(self.file.url[1:]))
		with open(f_name,'w',encoding='utf-8') as obj:
			obj.write(str(words.replace('“','"')))
	

	def saveLocally(self,words,path=None):
		if self.folder:
			f_nam=str(self.folder.local_path)
		else:
			f_nam=path
		f_name=str(BASE_DIR.joinpath(f_nam  +'/' + self.name))
		with open(f_name,'w',encoding='utf-8') as obj:
			obj.write(words)
		
		return


	def get_absolute_url(self):
		#support code ,video , music
		return reverse('FileDetailViewUrl',args=[self.id])
		
	def createBranch(self,owner):
		b=File.objects.get(id=self.id)
		u=b.folder
		word=b.openFile()
		con=ContentFile(word, f'branch_{self.name}')
		j=File.objects.create(name=self.name,folder=self.folder,file=con,edited=b,edit_owner=owner)
		return reverse('BranchUrl',args=[self.id])
		
	def Clone(self,owner,folder):
		b=File.objects.get(id=self.id)
		u=b.folder
		print('from models',self.name)
		j=File.objects.create(name=self.name,folder=folder,file=self.file,clone=True)
		return
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



@receiver(post_save, sender=User)
def ProfileCreated(sender, created, instance,**kwargs):
    if created:
        Profile.objects.create(user=instance)

# @reciver(post_save,sender=File)
# def OwnerFile(sender,created,instance,**kwargs):
# 	if created:
# 		instance.owner = instance.folder.owner