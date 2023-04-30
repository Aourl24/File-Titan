from django.contrib import admin
from .models import Folder, File, Profile

admin.site.register([Folder,File, Profile])
