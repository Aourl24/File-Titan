from django.shortcuts import render
from .models import Company, Pricing, PreviousWork,Info
from portfolio.models import Project
from blog.models import Post
from django.views.decorators.cache import never_cache
from django.core.paginator import Paginator

@never_cache
def View(request):
	company=Company.objects.all()
	price=Pricing.objects.all()
	project=Project.objects.all().order_by('-id')[:3]
	previous_work=PreviousWork.objects.all()
	info=Info.objects.all()
	templates=['companyTemplate/index.html','companyTemplate/skillandtech.html','companyTemplate/personalinfo.html','companyTemplate/recentprojects.html']
	page=request.GET.get('page')
	paged_template=Paginator(templates,1)
	template_page=paged_template.get_page(page)
	template=template_page.object_list
	template=template[0]
	if template_page.has_next():
		page_count=template_page.next_page_number
	else:
		page_count=None
	# if page_count == len(templates):
	# 	page_count=None

	context=dict(company=company,price=price,previous=previous_work,info=info, project=project,page_count=page_count)
	return render(request,template,context)
	

def SearchView(request):
    b=request.GET['search']
    project=Project.objects.filter(title__icontains=b)
    info=Info.objects.all()
    post=Post.objects.filter(title__icontains=b)
    #result=project.union(post)
    
    template='companyTemplate/search.html'
    context=dict(post=post, project=project)
    return render(request, template, context)