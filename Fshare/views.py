from django.shortcuts import render,redirect
from django.urls import reverse
from .models import Folder,File, Profile,Header,SubHeader
from .form import FolderForm,FileForm,EditUser,EditFolder
from django.http import StreamingHttpResponse,HttpResponse,HttpResponseRedirect
from .decorators import CheckAccess
from django.core.files.base import ContentFile
from django.core.exceptions import ObjectDoesNotExist
import subprocess
from FileShare.settings import BASE_DIR
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

Error="<div class='message' id='message'>Unable to Perform Action, Check your Path </div>"
Saved="<div class='' id='msg' style=''> Saved </div>"
t='FshareTemplate/'
#POST https://titleId.playfabapi.com/File/GetFiles
def landingView(request):
	# The landing page
	header=Header.objects.all()
	context=dict(headers=header)
	return render(request, 'index.html',context)

def folderListView(request):
	#This function display all folder both public and authorize
	if request.user.is_authenticated:
		prof=Profile.objects.get(user=request.user)
	else:
		prof=''
	folders=Folder.objects.all().filter(privacy__in=['public','authorize']).filter(parent=None).select_related('owner')# | Folder.objects.filter(privacy='authorize').filter(parent=None).select_related()
	#filter all folders that are public and authorize
	pageFolder=Paginator(folders,5) #Group the folder into 5 so has to reduce overhead
	page_no=request.GET.get('page_no')
	page=pageFolder.get_page(page_no)
	template=t+'home.html'
	if 'HX-Request' in request.headers: # if the request is ajax i.e from htmx, definitely the template is folderlist.html
		template=t + 'folderlist.html'
	context=dict(folders=page,prof=prof)
	return render(request,template,context)

def createFileView(request):
	#This function create new file
	if request.method == 'POST':
		file_name=request.POST.get('filename')
		d=request.POST.get('folderid')
		folder=Folder.objects.get(id=d)
		file_created=File.objects.create(name=str(file_name),folder=folder,file=ContentFile(b'',name=f'{file_name}'))
	template=t + 'create.html'
	return HttpResponseRedirect(reverse('FileDetailViewUrl',kwargs={'id':file_created.id}))


@login_required(login_url='login')
def FileFormView(request):
	Ff=FileForm()
	template=t+'index.html'
	if request.method == 'POST':
		Ff=FileForm(request.POST,request.FILES)
		others=request.FILES.getlist('file')
		if Ff.is_valid():
			if 'folder' in request.POST:
				fod=request.POST.get('folder')
				for files in others:
					file=File.objects.create(name=files.name,file=files,folder=Folder.objects.get(id=fod))
				return redirect('FolderDetailViewUrl',fid=int(fod))

			else:
				for files in others:
					file=File.objects.create(name=files.name,file=files)
			file.save()
			return redirect('FileViewUrl')
	context=dict(fileForm=Ff)
	return render (request,template,context)


@login_required
def FolderFormView(request):
	folderForm=FolderForm()
	fileForm=FileForm()
	template=t+'folder.html'
	context=dict(form=folderForm,filform=fileForm)

	if request.method == 'POST':
		folderForm=FolderForm(request.POST)
		folder_id=request.POST.get('folderid')
		
		if folderForm.is_valid():
			fod=folderForm.save(commit=False)
			#check=folderForm['privacy'].value()
			privacy = request.POST.get('privacy')
			print(privacy)
			fod.privacy = privacy
			#print(check)
			if privacy == 'authorize':
				password=request.POST.get('password')
				confirm_password=request.POST.get('confirm_password')
				print(password)
				if password == '':
					folderForm=FolderForm(instance=fod)
					context['warning']='You are required to set a password since your directory is authorize'
					context['folderForm']=FolderForm(instance=fod)
					return render(request,template,context)
				elif password != confirm_password:
					context['warning']='Your Password does not match, kindly check your password'
					context['folderForm']=FolderForm(instance=fod)
					return render(request,template,context)
				else:
					fod.password=password
			
			fod.owner=Profile.objects.get(user=request.user)
			if folder_id:
				fod.parent=Folder.objects.get(id=folder_id)
			fod.save()
		return redirect('FolderDetailViewUrl', fid=fod.id)	
	return render(request,template,context)



def FileDetailView(request,id=None,allow=False,typ=None):
	Ff=''
	file=''
	template=''
	real_file=''
	prof=''
	code_file=''
	video_file=''
	audio_file=''
	unknown_file = ''
	folderform=FolderForm()
	if request.user.is_authenticated:
		prof=Profile.objects.get(user=request.user)
	if id:
		file=File.objects.get(id=id)
		if file.edit_owner:
			if file.edit_owner == prof:
				allow=True
			else:
				allow=False
		else:
			if file.folder.owner == prof:
				allow=True
			else:
				allow=False

		template=t + 'filedetail.html'
		if file.name.endswith('.mp4') or typ == 'video':
			video_file = True
		elif file.name.endswith('.mp3') or typ == 'audio':
			audio_file = True
		elif file.name.endswith('.py') or typ == 'code':
			code_file = True
		else:
			unknown_file = True 

		if request.method== 'POST':
 
			b=request.POST.get('word')
			
			if request.user.is_authenticated:
				prof=Profile.objects.get(user=request.user)
				if file.folder.owner != prof:
					folder=Folder.objects.get(id=file.folder.id)
					edit_word=ContentFile(b,name=f'{request.user}_branch_{file.name}')
					
					try:
						edit_file=File.objects.get(name=f'{file.name}',edit_owner=prof)
						edit_file.saveFile(str(b))

					except ObjectDoesNotExist:
						edit_file=File.objects.create(file=edit_word, edited=file, edit_owner=prof ,folder=file.folder,name=f'{file.name}' )
					edit_file.saveFile(str(b))

					return HttpResponse("<div class='message' id='message'>Branch Saved </div>")

				else:
					file.saveFile(str(b))
					print('we are saving')
					return HttpResponse(Saved)
			else:
				return HttpResponse('You can not save file because you are not logged in')
			
			# if 'path' in request.POST:
			# 	b=request.POST.get('word')
			# 	c=request.POST.get('path')
			# 	try:
			# 		file.saveLocally(str(b),c)
			# 	except:
			# 		params={'HX-Target':'#feedback','HX-Swap':'innerHTML'}
			# 		return HttpResponse(Error)

			return HttpResponse(Saved)
	
	context=dict(file=file,audio_file=audio_file,code_file=code_file,video_file=video_file,unknown_file=unknown_file,fileForm=Ff,originalFile=real_file,prof=prof,form=folderform,allow=allow)
	return render(request,template,context) 

@CheckAccess
def folderDetailView(request,fid):
	if fid:
		file=Folder.objects.get(id=fid)
		child_files = file.file.all()
		form=FileForm()
		template=t + 'folderdetail.html'
		Ff=FileForm()
		folderform=FolderForm()

		if request.user.is_authenticated:
			prof=Profile.objects.get(user=request.user)
		else:
			prof=''

		real_file=file.file.filter(edited=None)
		if request.method=='POST':

			if 'path' in request.POST:
				path=request.POST.get('path')
				file.local_path=path
				file.save()

	context = dict(file=file,originalFile=child_files,prof=prof,fileForm=form,form=folderform)
	return render(request,template,context)

def DeleteView(request,id=None,fid=None):
	real_file=''

	if request.user.is_authenticated:
		prof=Profile.objects.get(user=request.user)
	else:
		prof=''

	if id:
		file=File.objects.get(id=id)
		file.Delete()
		
		if 'folderId' in request.GET:
			file=Folder.objects.get(id=request.GET.get('folderId'))
			real_file=file.file.filter(edited=None)
		context=dict(originalFile=real_file,prof=prof)
		return render(request,t+'file.html',context)

	if fid:
		fod=Folder.objects.get(id=fid)
		parent=fod.parent
		fod.Delete()
		if parent:
			return redirect('FolderDetailViewUrl',fid=parent.id)


	return redirect('FileViewUrl')


def CloneView(request,id):
	f=File.objects.get(id=id)
	profile=Profile.objects.get(user=request.user)
	if request.method == 'POST':
	    fname=request.POST.get('foldername')
	    folder=Folder.objects.get(name=fname,owner=profile)
	    #f.folder=folder
	    #f.save()
	    print('from view1',f.name)
	    f.Clone(profile, folder)
	return HttpResponse("<div class='container color-bg-s color-white'>File cloned Successfully</div>")
	
def cloneFolder(request, id):
    f=File.objects.get(id=id)
    print('from view2',f.name)
    template=t + 'confirm.html'
    profile=Profile.objects.get(user=request.user)
    folder=Folder.objects.filter(owner=profile)
    context=dict(file=f, folder=folder)
    return render(request, template, context) 

def EditorView(request,id=None):

	context=dict()
	return JsonResponse(context)

def giveAcessView(request, id=None):
	
	Error=''

	if request.method == 'POST':
		password=request.POST.get('password')
		passw=Folder.objects.get(id=id).password
		print(password,passw)
		if passw == password:
			request.session[f'folder{id}']='allow'
			return redirect('FolderDetailViewUrl',fid=id)
		
		else:
			Error="Wrong Password"
			#return (request.path_info)

	context=dict(Error=Error)

	return render(request, t+'access.html',context)

def branchView(request,id):
	if request.user.is_authenticated:
	    prof=Profile.objects.get(user=request.user)
	else:
	    prof=''
	file=File.objects.get(id=id)
	if file.edit_owner:
		owner=file.edit_owner.user.username
	else:
		owner='Unknown'
	context=dict(file=file,prof=prof,owner=owner)

	return render(request, t+'branch.html',context)

def shellView(request,id):
	file=File.objects.get(id=id)
	if file.name.endswith('.py'):
		word=file.openFile()
		print(file.file.url)
		result=subprocess.getoutput(f" python {BASE_DIR.joinpath('')}/{file.file.url} ")
		res=result.split()
		result=(' ').join(res)
		context=dict(file=file,output=result)

		return render(request, t+'shell.html',context)
	else:
		return HttpResponse('File is not Executable')

def createBranch(request,id):
	f=File.objects.get(id=id)
	prof=Profile.objects.get(user=request.user)
	return HttpResponseRedirect(f.createBranch(prof))

def replaceView(request,id,bid):
	f=File.objects.get(id=id)
	m=File.objects.get(id=bid)
	f.replace(bid)
	return HttpResponse(f"<div class='message' id='message' style='width:90%'>You have succesfull Replace the Original File with {m.name}</div>")

def mergeView(request,id,bid):
	f=File.objects.get(id=id)
	m=File.objects.get(id=bid)
	f.merge(bid)
	return HttpResponse(f"<div class='message' style='width:90%' id='message'>You have succesfull merge this branch with the Original File - {m.name}</div>")


def profileView(request,id=None):
	if id is None:
		profile=Profile.objects.get(user=request.user)
	else:
		profile=Profile.objects.get(id=id)
	template=t + 'profile.html'
	try:
		branch_file=File.objects.filter(edit_owner=profile)
	except ObjectDoesNotExist:
		branch_file=[{'error':'There is no branch files'}]
	file={'id':2}
	context=dict(profile=profile,branches=branch_file,file=file)
	return render(request,template,context)

def profileEdit(request):
	prof=Profile.objects.get(user=request.user)
	editForm=EditUser(instance=prof)
	template=t + 'editprofile.html'
	if request.method == 'POST':
		new_name=request.POST.get('username')
		editForm=EditUser(request.POST,request.FILES,instance=prof)
		if editForm.is_valid():
			a=editForm.save(commit=False)
			a.user.username=new_name
			a.save()

		return redirect('ProfileUrl',id=prof.id)
	template= t + 'profileedit.html'
	context=dict(form=editForm,profile=prof)
	return render(request,template,context)

def importFile(request):
	c=''
	if request.method == 'POST':
		#d=request.POST['importfile']
		b=request.FILES.get('importfile')
		print(b)
		if b is None:
			raise ImportError

		c=request.POST.get('filename')
		file=File.objects.get(id=c)
		file.file=b
		file.save()

		return redirect('FileDetailViewUrl',id=c)

def searchFile(request):
	if request.method == 'POST':
		b=request.POST.get('search')
		result_file=File.objects.filter(name__icontains=b)
		result_folder=Folder.objects.filter(name__icontains=b)
		template=t +'search.html'
		context=dict(result_files=result_file,result_folders=result_folder)
		return render (request,template,context)


def menuView(request):
	#files=File.objects.all()
	if request.user.is_authenticated:
		prof=Profile.objects.get(user=request.user)
		folders=Folder.objects.filter(owner=prof)
		context=dict(folders=folders)
	else:
		context=dict(warning='Anonymous user are not allowed to use this function')
	template=t+'menu.html'
	return render(request,template,context)


def deleteBranch(request,id):
	file=File.objects.get(id=id)
	parent_file=file.edited.id
	file.Delete()
	return redirect('BranchUrl',id=parent_file)

def downloadView(request,id):
	folder = Folder.objects.get(id=id)
	context=dict(folder=folder)
	return render(request,t+'download.html',context)


def confirm(request):
	return render(request,t+'confirmA.html',context)

def editFolder(request,id=None,next=None):
	folder=Folder.objects.get(id=id)
	form = EditFolder(instance=folder)
	template = t+'editFolder.html'
	context=dict(folder=folder,form=form)

	if request.method == 'POST':
		form = EditFolder(request.POST,instance=folder)
		if form.is_valid():
			b=form.save(commit=False)
			c=request.POST.get('privacy')
			b.privacy = c
			if c == 'authorize':
				d = request.POST.get('password')
				e = request.POST.get('confirm_password')
				if d == e:
					b.password = d
				else:
					context['error'] = 'Your Password does not correspond,kindly check again'
					return render(request,template,context)
			b.save()
		return redirect(next)

	return render(request,template,context)
	
def darkView(request,path):
    if 'dark' in request.session.keys():
        del request.session['dark']
    else:
        request.session['dark'] = True
    return redirect(path)