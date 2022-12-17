from django.urls import path,include
from .views import FileView,FileFormView,FileDetailView,FolderFormView,DeleteView,CloneView,\
giveAcessView,createView,branchView,shellView,createBranch, replaceView , mergeView,profileView,profileEdit,landingView, \
cloneFolder,importFile,searchFile,menuView,deleteBranch
from django.conf.urls.static import static
from django.conf import settings

urlpatterns=[
	path('',landingView,name='LandingUrl'),
	path('fileform',FileFormView,name='FileFormUrl'),
	path('file',FileView,name='FileViewUrl'),
	path('<int:id>',FileDetailView,name='FileDetailViewUrl'),
	path('<int:fid>folder',FileDetailView,name='FolderDetailViewUrl'),
	path('folderform',FolderFormView,name='FolderFormUrl'),
	path('<int:fid>delete',DeleteView,name='FolderDeleteUrl'),
	path('<int:id>del',DeleteView,name='FileDeleteUrl'),
	path('<int:id>clone',CloneView,name='CloneUrl'),
	path('<int:id>clfolder', cloneFolder, name='CloneFolderUrl'), 
	path('giveacess<int:id>',giveAcessView,name='GiveAcessUrl'),
	path('create',createView,name='CreateUrl'),
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
	path('deleteBranch<int:id>',deleteBranch,name='DeleteBranchUrl')
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
