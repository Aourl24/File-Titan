from django.contrib import admin
from .models import Folder, File, Profile,Notify,Activity
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

admin.site.unregister(Site)
admin.site.unregister(User)

class SiteModel(admin.ModelAdmin):
    list_display = ['id','name','domain']

class ProfileModel(admin.StackedInline):
    model = Profile

class UserModel(admin.ModelAdmin):
    model = User
    inlines = [ProfileModel]

class FileModel(admin.StackedInline):
	model = File

class FolderModel(admin.ModelAdmin):
	model= Folder
	inlines = [FileModel]

admin.site.register(Site,SiteModel)
admin.site.register(User,UserModel )
admin.site.register(Folder,FolderModel)
admin.site.register([File, Profile,Notify,Activity])
