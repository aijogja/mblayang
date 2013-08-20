# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.db.models import Q
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
        'home' : True,
        'all_category' : Kategori.objects.all().order_by('kategori'),
    }

def home(request):
	return render_to_response('index.html','', context_instance=RequestContext(request, processors=[home_custom_proc]))

def cari(request):
    if request.method == 'POST':    # ketika submit data  
        hasil = []
        cari = request.POST['cari']
        wisata = Wisata.objects.filter(Q(nama__icontains = cari) | Q(description__icontains = cari))
        for h in wisata:
            hasil.append({'nama':h.nama, 'detail':'/wisata/'+ str(h.id), 'jenis':'Wisata'})

        news = News.objects.filter(Q(title__icontains = cari) | Q(description__icontains = cari))
        for h in news:
            hasil.append({'nama':h.title, 'detail':'/news/'+ str(h.id), 'jenis':'News'})

        datanya = {'hasil' : hasil}
        return render_to_response('cari.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))
    else :
        return HttpResponseRedirect('/')


