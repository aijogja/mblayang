# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from apps.wisata.models import Wisata, Kategori
from apps.news.models import News

def custom_proc(request):
    return {
        'title': 'mBlayang',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'slide_show' : Wisata.objects.all(),
        'top_news' : News.objects.all().order_by('-hit')[:2],
        'top_wisata' : Wisata.objects.all().order_by('-hit')[:2],
        'all_category' : Kategori.objects.all().order_by('kategori'),
    }

def home_custom_proc(request):
    return {
        'title': 'mBlayang',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'slide_show' : Wisata.objects.all(),        
        'top_news' : News.objects.all()[:3],
        'home' : True
    }

def home(request):
	return render_to_response('index.html','', context_instance=RequestContext(request, processors=[home_custom_proc]))


