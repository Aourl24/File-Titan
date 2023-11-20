from django.db import models
from django.urls import reverse
from FileShare.settings import BASE_DIR,MEDIA_ROOT
from django.http import StreamingHttpResponse,HttpResponse,FileResponse
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from django.core.files.base import ContentFile
from datetime import datetime
import zipfile
from django.conf  import settings
from django.core.files import File
from django.core.files.storage import storages
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
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
    try:
      path = f'{root.name}/'
    except:
      return f"file/{filename}"
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
    size=models.IntegerField(default=0)
    max_size=models.IntegerField(default=26214400)

    def __str__(self):
        return self.user.username
        
    def get_absolute_url(self):
        return reverse('ProfileUrl', args=[self.id])

    def check_size(self):
    	if self.size > self.max_size:
    		print(self.size)
    		return False
    	return True

    def size_in_percent(self):
    	percent = (self.size/self.max_size) * 100
    	return int(percent)
    	
    def unread_notification(self):
      return Notify.objects.filter(profile=self,read=False)

class Activity(models.Model):
  profile = models.ForeignKey(Profile,related_name='activity',on_delete=models.CASCADE)
  datetime = models.DateTimeField(auto_now_add=True)
  body = models.TextField()
  
  def __str__(self):
    return self.profile.user.username + ' activities'

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

 # def main_files(self):
   # return File.objects.filter(folder=self).exclude(edited)
	
	def Delete(self):
		files_in_folder = self.file.all()
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
	file=models.FileField(upload_to=upload_file,blank=True,null=True)
	content=models.TextField(null=True,blank=True)
	edited=models.ForeignKey('self',related_name='edited_file',blank=True,null=True,on_delete=models.CASCADE)
	edit_owner=models.ForeignKey(Profile,null=True,blank=True,related_name='my_file_edit',on_delete=models.CASCADE)
	date_created=models.DateTimeField(auto_now_add=True)
	last_updated=models.DateTimeField(auto_now=True)
	clone=models.BooleanField(default=False)
	file_type = models.CharField(max_length=100000,default='txt')
    
	def __str__(self):
		return self.name

	def Delete(self):
		size_of_file = self.file.file.size
		file=File.objects.get(id=self.id)
		try:
			file.file.delete()
		except:
			pass
		file.delete()
		prof = self.folder.owner
		prof.size -= size_of_file
		prof.save()
		return
		#return reverse('FileViewUrl')
		
	def openFile(self):
		path = f"{MEDIA_ROOT}"
		# try:
		# 	a = self.file.read()
		# except FileNotFoundError:
		# 	print(self.file.name)
		# 	with open(f"{path}/{self.file.name}",'r') as obj:
		# 		a = obj.read()
		return self.content
		
	def branch(self):
		return reverse('BranchUrl',args=[self.id])

	def saveFile(self,words):
		words=words.replace('”','"')
		self.content = words
		self.save()
				
	def saveLocally(self,words,path=None):
		pass

	def get_absolute_url(self):
		#support code ,video , music
		return reverse('FileDetailViewUrl',args=[self.id])
		
	def createBranch(self,owner):
		b=File.objects.get(id=self.id)
		u=b.folder
		word=b.openFile()
		#con=ContentFile(word, f'branch_{self.name}')

		j=File.objects.create(name=self.name,folder=self.folder,content=word,edited=b,edit_owner=owner)
		Notify.objects.create(profile=self.folder.owner,sender=owner,body='Someone create a branch for your file')
		return reverse('BranchUrl',args=[self.id])
		
	def Clone(self,owner,folder):
		b=File.objects.get(id=self.id)
		u=b.folder
		print('from models',self.name)
		j=File.objects.create(name=self.name,folder=folder,file=self.file,content=self.content,clone=True)
		Notify.objects.create(profile=self.folder.owner,sender=folder.owner, body='someone clone one of your files in your folder')
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

class Notify(models.Model):
  profile = models.ForeignKey(Profile,related_name='profile_notify',on_delete=models.CASCADE)
  sender = models.ForeignKey(Profile,related_name='sender_notify',on_delete=models.CASCADE)
  body = models.CharField(max_length=100000)
  #body = models.TextField()
  time = models.DateTimeField(auto_now_add=True)
  read = models.BooleanField(default=False)

  def __str__(self):
    return self.profile.user.username + ' Notification' 
  
  def unread(self):
    return ['apple' ]
    #return self.objects.filter(read=False)
  
@receiver(post_save, sender=User)
def ProfileCreated(sender, created, instance,**kwargs):
    if created:
        prof=Profile.objects.create(user=instance)
        folder = Folder.objects.create(owner=prof,name='Sample Folder')

@receiver(pre_save,sender=File)
def FileCreated(sender,instance,**kwargs):
	#if created:
	
	if instance.content:
		try:
			with instance.file.open('w') as file:
				file.write(instance.content)
		except:
			file_created = ContentFile(instance.content,name=f'{instance.name}')
			instance.file = file_created


@receiver(post_save,sender=File)
def FileType(sender,created,instance,**kwargs):
  if created:
    try:
      if instance.file:
        file_ext = instance.file.name.split('.')
      else:
        file_ext = instance.name.split('.')
      extension = file_ext[-1]
    except AttributeError:
      extension = 'txt'
    instance.file_type = extension
    instance.save()
    
# @receiver(post_save,sender=File)
# def ClonesFile(sender,created,instance,**kwargs):
#   if instance.edited:
#     print('signal working')
#     clones = instance.edited.all()
#     print(clones)
#     for clone in clones:
#       clone.content = instance.content
#       clone.save()