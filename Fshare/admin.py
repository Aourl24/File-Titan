from django.contrib import admin
from .models import Folder, File, Profile
from django.contrib.auth.models import User
admin.site.unregister(User)

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
	
admin.site.register(User,UserModel )
admin.site.register(Folder,FolderModel)
admin.site.register([File, Profile])
