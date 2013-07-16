# Create your views here.

from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from apps.news.models import News
from apps.news.forms import AddNewsForm
from mblayang.views import custom_proc
from apps.wisata.models import get_file_path
    
def news_index(request):
    try:
        list_news = News.objects.all().order_by('-id')[:5]
    except News.DoesNotExist:
        list_news = ''
    
    return render_to_response('news/news_view.html',{'list_news':list_news, 'slide_show' : False}, context_instance=RequestContext(request, processors=[custom_proc]))        

def news_all(request):
    try:
        list_news = News.objects.all().order_by('-id')
    except News.DoesNotExist:
        list_news = ''
    
    return render_to_response('news/news_view.html',{'list_news':list_news, 'slide_show' : False}, context_instance=RequestContext(request, processors=[custom_proc]))

def news_detail(request, id_news):    
        detail = get_object_or_404(News, pk=id_news)            
        breadcrumb = 'Detail'

        detail.hit += 1
        detail.save()    

        datanya = {'latest_news':detail, 'slide_show' : False, 'breadcrumb': breadcrumb}
        return render_to_response('news/news_view.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def news_add(request):
    if request.method == 'POST':                # ketika submit data
        form = AddNewsForm(request.POST, request.FILES)       # isi value pada form sesuai yg di POST
        if form.is_valid():             # cek validasi
            # Data ada di array form.cleaned_data           
            user = User.objects.get(pk=request.user.id)
            news = News()
            news.nama = form.cleaned_data['title']
            news.description = form.cleaned_data['description']
            news.member = user
            
            if request.FILES:
                f = request.FILES['image']          
                path = get_file_path(request,f.name)
                fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path)), 'wb')
                for chunk in f.chunks():
                    fd.write(chunk)
                fd.close()  
            else :
                path = ''
            
            news.image = path
            news.save()                       #insert data ke table news
            
            messages.success(request, "Add News Success.")
            return HttpResponseRedirect('/news/')        # Redirect after POST
            #return render_to_response('wisata/form_wisata.html',{'tulisan':tulisan}, context_instance=RequestContext(request, processors=[custom_proc]))       
    else:
        form = AddNewsForm()          # value form kosongan

    breadcrumb = 'Add News'
    datanya = {'form':form, 'breadcrumb': breadcrumb}
    return render_to_response('news/form_news.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))