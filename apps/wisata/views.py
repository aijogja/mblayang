# Create your views here.

from django.shortcuts import render_to_response, render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.db.models import Count
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.decorators.csrf import csrf_exempt
from apps.wisata.models import Wisata, Kategori, Comment, Like, Gallery, Kota, Laporkan, get_file_path
from apps.wisata.forms import AddWisata, CommentForm, AddGallery
from mblayang.views import custom_proc

def wisata_index(request):
	latest_wisata = Wisata.objects.annotate(num_comment=Count('comment', distinct=True)).annotate(num_like=Count('like', distinct=True)).order_by('-id')[:5]

        datanya = {'latest_wisata': latest_wisata}
	return render_to_response('wisata/wisata_view.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))		

def wisata_all(request):
    wisata_list = Wisata.objects.annotate(num_comment=Count('comment', distinct=True)).annotate(num_like=Count('like', distinct=True)).order_by('-id')
    paginator = Paginator(wisata_list, 10) # Show 10 object per page

    page = request.GET.get('page')
    try:
        wisata = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        wisata = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        wisata = paginator.page(paginator.num_pages)

    datanya = {'latest_wisata': wisata, 'pagination' : True}
    return render_to_response('wisata/wisata_view.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

def wisata_category(request, category):   
    latest_wisata = Wisata.objects.filter(kategori__kategori=category).annotate(num_comment=Count('comment', distinct=True)).annotate(num_like=Count('like', distinct=True))
    slide_show = Wisata.objects.filter(kategori__kategori=category)
    breadcrumb = 'Kategori'

    datanya = {'latest_wisata': latest_wisata, 'slide_show': slide_show, 'breadcrumb': breadcrumb}
    return render_to_response('wisata/wisata_view.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

def wisata_detail(request, id_wisata):    
        detail = get_object_or_404(Wisata, pk=id_wisata)
        comment = Comment.objects.select_related().filter(wisata=id_wisata)
        likenya = Like.objects.select_related().filter(wisata=id_wisata)        
        gallery = Gallery.objects.select_related().filter(wisata=id_wisata, visible=1)
        breadcrumb = 'Detail'

        detail.hit += 1
        detail.save()

        exis = None
        if request.user.is_authenticated():
            try:
                exis = Like.objects.get(user=request.user,wisata=id_wisata)
            except Like.DoesNotExist:
                exis = None
        
        like = {'count':likenya.count,'exist':exis}

        laporan = None
        if request.user.is_authenticated():
            try:
                laporan = Laporkan.objects.get(user=request.user,wisata=id_wisata)
            except Laporkan.DoesNotExist:
                laporan = None        
        
        if request.method == 'POST':                # ketika submit data
            form = CommentForm(request.POST, request.FILES)   
            if form.is_valid():
                # Data ada di array form.cleaned_data
                user = User.objects.get(pk=request.user.id)
                wisata = Wisata.objects.get(pk=id_wisata)
                comment = Comment()
                comment.user = user
                comment.wisata = wisata
                comment.comment = form.cleaned_data['comment']
                comment.save()
                return HttpResponseRedirect(request.build_absolute_uri())

        else:
            form = CommentForm()             # value form kosongan
    
        datanya = {'wisata':detail, 'comment':comment, 'like':like, 'gallery':gallery, 'form':form, 'slide_show' : False, 'breadcrumb': breadcrumb, 'laporan':laporan}
        return render_to_response('wisata/wisata_detail.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def like(request, id_wisata):
    user = User.objects.get(pk=request.user.id)
    wisata = Wisata.objects.get(pk=id_wisata)     
    like = Like.objects.get_or_create(user=user,wisata=wisata,like=True)
        
    return HttpResponseRedirect('/')

@login_required
def unlike(request, id_wisata):
    user = User.objects.get(pk=request.user.id)
    wisata = Wisata.objects.get(pk=id_wisata)     
    try:
        like = Like.objects.get(user=user,wisata=wisata)
        like.delete()
    except Like.DoesNotExist:
        pass
        
    return HttpResponseRedirect('/')

@login_required
def add_wisata(request):
    if request.method == 'POST':    # ketika submit data
        form = AddWisata(request.POST, request.FILES)       # isi value pada form sesuai yg di POST
        if form.is_valid():
            # Data ada di array form.cleaned_data
            user = User.objects.get(pk=request.user.id)
            kota = Kota.objects.get(pk=form.cleaned_data['kota'])
            wisata = Wisata()
            wisata.nama = form.cleaned_data['nama']
            wisata.description = form.cleaned_data['description']
            wisata.location = form.cleaned_data['location']
            wisata.member = user
            wisata.kategori = form.cleaned_data['kategori']
            wisata.propinsi = form.cleaned_data['propinsi']
            wisata.kota = kota         
            
            f = request.FILES['image']          
            path = get_file_path(request,f.name)
            fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path)), 'wb')
            for chunk in f.chunks():
                fd.write(chunk)
            fd.close()              
            
            wisata.image = path
            wisata.save()                       #insert data ke table wisata

            messages.success(request, "Add Wisata Success.")
            return HttpResponseRedirect('/wisata')      # Redirect after POST

    else :
        form = AddWisata()

    breadcrumb = 'Add Wisata'
    datanya = {'form' : form,'breadcrumb': breadcrumb}
    return render_to_response('wisata/form_wisata.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

def get_city(request, id_propinsi):   
    kota = Kota.objects.all().filter(propinsi=id_propinsi)
    json = serializers.serialize('json', kota)

    return HttpResponse(json, mimetype='application/json')

"""
@login_required
def add_sukses(request):
	tulisan = "Data sudah tersimpan."

        datanya = {'tulisan':tulisan}
	return render_to_response('wisata/form_wisata.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))
"""

@login_required
def add_gallery(request, id_wisata):
    if request.method == 'POST':                # ketika submit data
        form = AddGallery(request.POST, request.FILES)       # isi value pada form sesuai yg di POST
        if form.is_valid():             # cek validasi
            # Data ada di array form.cleaned_data           
            user = User.objects.get(pk=request.user.id)
            wisata = Wisata.objects.get(pk=id_wisata) 
            galery = Gallery()
            galery.member = user
            galery.wisata = wisata
            galery.visible = form.cleaned_data['visible']

            f = request.FILES['image']          
            path = get_file_path(request,f.name)
            fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path)), 'wb')
            for chunk in f.chunks():
                fd.write(chunk)
            fd.close()  
            
            galery.image = path
            galery.save()   

            messages.success(request, "Add Gallery Success.")
            return HttpResponseRedirect('/wisata/'+ id_wisata)        # Redirect after POST
    else:
        form = AddGallery()          # value form kosongan

    breadcrumb = 'Add Gallery'
    datanya = {'form':form, 'breadcrumb': breadcrumb}
    return render_to_response('wisata/form_gallery.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
@csrf_exempt
def laporkan(request):
    if request.method == "POST" and request.is_ajax:
        laporkan = Laporkan()
        wisata = Wisata.objects.get(pk=request.POST["wisata_id"]) 

        laporkan.user = request.user
        laporkan.wisata = wisata
        laporkan.alasan = request.POST["alasan"]
        laporkan.save()
        msg = "Sukses."
        
    else:
        msg = "Ajax Post only."

    return HttpResponse(msg)