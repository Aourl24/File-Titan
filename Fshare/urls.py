from django.urls import path,include
from .views import folderListView,FileFormView,FileDetailView,FolderFormView,DeleteView,CloneView,\
giveAcessView,createFileView,branchView,shellView,createBranch, replaceView , mergeView,profileView,profileEdit,landingView, \
cloneFolder,importFile,searchFile,menuView,deleteBranch,downloadView,editFolder, folderDetailView, darkView
from django.conf.urls.static import static
from django.conf import settings

def filt(x):
	b=x.replace('/','')
	return str(b)

urlpatterns=[
	#path('',landingView,name='LandingUrl'),
	path('fileform',FileFormView,name='FileFormUrl'),
	path('',folderListView,name='FileViewUrl'),
	path('<int:id>',FileDetailView,name='FileDetailViewUrl'),
	path('<int:id>/<str:typ>',FileDetailView,name='FileDetailViewTypeUrl'),
	path('<int:fid>folder',folderDetailView,name='FolderDetailViewUrl'),
	path('folderform',FolderFormView,name='FolderFormUrl'),
	path('<int:fid>delete',DeleteView,name='FolderDeleteUrl'),
	path('<int:id>del',DeleteView,name='FileDeleteUrl'),
	path('<int:id>clone',CloneView,name='CloneUrl'),
	path('<int:id>clfolder', cloneFolder, name='CloneFolderUrl'), 
	path('giveacess<int:id>',giveAcessView,name='GiveAcessUrl'),
	path('create',createFileView,name='CreateUrl'),
	path('branch<int:id>',branchView,name='BranchUrl'),
	path('shell<int:id>',shellView, name='ShellUrl'),
	path('createBranch<int:id>',createBranch,name='CreateBranchUrl'),
	path('replace<int:id>with<int:bid>',replaceView,name='ReplaceUrl'),
	path('merge<int:id>with<int:bid>',mergeView,name='MergeUrl'),
	path('profile<int:id>',profileView,name='ProfileUrl'),
	path('prof',profileEdit,name='ProfileEditUrl'),
	path('import',importFile,name='ImportFileUrl'),
	path('search',searchFile,name='SearchUrl'),
	path('menu',menuView,name='MenuUrl'),
	path('profile',profileView,name='ProfileLandingUrl'),
	path('deleteBranch<int:id>',deleteBranch,name='DeleteBranchUrl'),
	path('download<int:id>',downloadView,name='DownloadUrl'),
	path('edit<int:id>folder<path:next>',editFolder,name='EditFolderUrl'),
	path("darkmode/<path:path>",darkView,name='DarkModeUrl')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
