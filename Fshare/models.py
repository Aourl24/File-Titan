from django.db import models
from django.urls import reverse
from FileShare.settings import BASE_DIR,MEDIA_ROOT
from django.http import StreamingHttpResponse,HttpResponse,FileResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from datetime import datetime
import zipfile
from django.conf  import settings
from django.core.files import File
from django.core.files.storage import storages
from django.core.files.storage import FileSystemStorage
from pathlib import Path
import cloudinary

# def select_storage():
#     if settings.AWS:
#         return storages['aws']
#     else:
#         return storages['default']
     
fs = FileSystemStorage(location=f"{BASE_DIR}/media")


def upload_file(self,filename):
    root = self.folder
    path = f'{root.name}/'
    while root.parent:
        path = root.parent.name + '/' + path
        root = root.parent
    print(path)
    return f"file/{path}/{filename}"

    
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
    profile_photo=models.ImageField(upload_to='profileimage', default='profileimage/profile.png', null=True, blank=True)
    mode=models.CharField(max_length=100, default='white')
    
    def __str__(self):
        return self.user.username
        
    def get_absolute_url(self):
        return reverse('ProfileUrl', args=[self.id])

class Folder(models.Model):
	owner=models.ForeignKey(Profile, related_name='folder', null=True, blank=True, on_delete=models.CASCADE)
	#profiles=models.ManyToManyField(Profile, blank=True, related_name='our_folder')
	name=models.CharField(max_length=10000)
	local_path=models.CharField(max_length=10000,default='C:/Users/USER/Documents/WDP/Django/',null=True,blank=True)
	parent=models.ForeignKey('self',related_name='child_folder',blank=True,null=True, on_delete=models.CASCADE)
	contributors=models.ManyToManyField(Profile, blank=True, related_name='our_folder')
	name=models.CharField(max_length=10000)
	cover_photo = models.ImageField(null=True,blank=True,upload_to='folder_cover_photos')
	parent=models.ForeignKey('self',related_name='child_folder',blank=True,null=True,
	on_delete=models.CASCADE)
	privacy=models.CharField(choices=[('public', 'public'), ('private', 'private'), ('authorize', 'authorize')], default='public', max_length=20)
	password=models.CharField(max_length=20, blank=True, null=True)
	date_created=models.DateTimeField(auto_now_add=True)
	last_updated=models.DateTimeField(auto_now=True)
	info=models.TextField('About Directory' ,null=True,blank=True)
	likes = models.ManyToManyField(Profile,related_name='folder_like',blank=True)
	download_count = models.IntegerField(default=0)

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
	    if not settings.LOCAL:
	        result = cloudinary.utils.download_folder(f"media/file/{self.name}",public_id = f'{self.name}', target_public_id = f"{self.name}", prefixes=f"{self.name}")
	        print(result)
	        return result
	    root= Path(f"{str(MEDIA_ROOT)}/file/{self.name}")
	    with zipfile.ZipFile(f"{MEDIA_ROOT}/zip/{self.name}.zip",mode="w") as archive:
	        for path in root.rglob("*"):
	            archive.write(path,arcname=path.relative_to(root))
	    self.download_count += 1
	    self.save()
	    return f'media/zip/{self.name}.zip'

class File(models.Model):
	folder=models.ForeignKey(Folder,related_name='file', on_delete=models.CASCADE,null=True,blank=True)
	name=models.CharField(max_length=10000)
	file=models.FileField(upload_to=upload_file,default='file/empty.txt')
	edited=models.ForeignKey('self',related_name='edited_file',blank=True,null=True,on_delete=models.CASCADE)
	edit_owner=models.ForeignKey(Profile,null=True,blank=True,related_name='my_file_edit',on_delete=models.CASCADE)
	date_created=models.DateTimeField(auto_now_add=True)
	last_updated=models.DateTimeField(auto_now=True)
	clone=models.BooleanField(default=False)
    
	def __str__(self):
		return self.name

	def Delete(self):
		File.objects.get(id=self.id).delete()
		return
		#return reverse('FileViewUrl')
		
	def openFile(self):
		path = f"{MEDIA_ROOT}"
		try:
			a = self.file.read()
		except FileNotFoundError:
			print(self.file.name)
			with open(f"{path}/{self.file.name}",'r') as obj:
				a = obj.read()
		return a
		
	def branch(self):
		return reverse('BranchUrl',args=[self.id])

	def saveFile(self,words):
		words=words.replace('”','"')
		try:
			self.file.open(mode='w')
			self.file.write(words)
			self.file.close()
		except FileNotFoundError:
			path = f"{MEDIA_ROOT}"
			with open(f"{path}/{self.file.name}",'w',encoding='utf-8') as obj:
				obj.write(str(words.replace('“','"')))
				
	def saveLocally(self,words,path=None):
		pass

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
		return "File clone successful"
		#return reverse('BranchUrl',args=[self.id])

	def replace(self,x):
		#b=File.objects.get(id=self.id)
		m=File.objects.get(id=x)
		word=m.openFile()
		try:
		    self.saveFile(word)
		except:
		    return "File is irreplaceable"
		return f"You have succesfull Replace the Original File with {m.name}"

	def merge(self,x):
		#b=File.objects.get(id=self.id)
		m=File.objects.get(id=x)
		d=self.openFile()
		k=m.openFile()
		try:
		    l=d.split('\n') + k.split('\n')
		    e=sorted(set(l),key=l.index)
		    v=('\n').join(e)
		    self.saveFile(v)
		except TypeError:
		    return "File does not support merge"
		return f"You have succesfull merge this branch with the Original File - {m.name}"



@receiver(post_save, sender=User)
def ProfileCreated(sender, created, instance,**kwargs):
    if created:
        prof=Profile.objects.create(user=instance)
        #prof.profile_photo = f"{MEDIA_ROOT}/profileimage/profile.png"
        # prof.save()
# @reciver(post_save,sender=File)
# def OwnerFile(sender,created,instance,**kwargs):
# 	if created:
# 		instance.owner = instance.folder.owner