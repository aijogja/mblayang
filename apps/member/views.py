# Create your views here.

from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils.dateformat import format, time
from django.conf import settings
from django.core.mail import send_mail
from apps.member.forms import RegistrasiForm, LoginForm, EditProfilForm, ChangePhotoForm
from apps.member.models import Profil, get_file_path
from apps.wisata.models import Gallery, Kota
from mblayang.views import custom_proc
import base64

def registrasi(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profil/')
	if request.method == 'POST':				# ketika submit data
		form = RegistrasiForm(request.POST)		# isi value pada form sesuai yg di POST
		if form.is_valid():				# cek validasi
			# Data ada di array form.cleaned_data	
			kota = Kota.objects.get(pk=form.cleaned_data['kota'])
			emailnya = form.cleaned_data['email']			
			user = User.objects.create_user(email = emailnya,	#create user
				username = form.cleaned_data['username'],
				password = form.cleaned_data['password']
			)
			user.is_active = False
			user.save()

			member = user.get_profile()
			member.nama = form.cleaned_data['nama']
			member.alamat = form.cleaned_data['alamat']
			member.tgl_lahir = form.cleaned_data['tgl_lahir']
			member.kota = kota
			member.propinsi = form.cleaned_data['propinsi']
			member.no_hape = form.cleaned_data['no_hape']
			member.gender = form.cleaned_data['gender']
			
			f = request.FILES['image']			
			path = get_file_path(request,f.name)
			fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path)), 'wb')
			for chunk in f.chunks():
				fd.write(chunk)
			fd.close()	
			
			member.foto = path
			member.save()						#insert data tambahan user ke member
			
			activatekey = base64.urlsafe_b64encode(emailnya)
			message = 'Aktifkan akun Anda dengan mengclick link berikut. <a href="'+ request.META['HTTP_HOST'] +'/activate/' + activatekey + '">Aktifkan</a>'
			send_mail('Aktivasi mBlayang Akun', message, 'no-reply@mblayang.com', [emailnya], fail_silently=False)
			
			messages.success(request, "Registrasi Success. Please cek your email to activate.")
			return HttpResponseRedirect('/wisata/') 		# Redirect after POST
	else:
		form = RegistrasiForm() 			# value form kosongan

	breadcrumb = 'Registrasi'
	datanya = {'form': form, 'breadcrumb': breadcrumb}
	return render_to_response('member/registrasi.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

"""
def sukses(request):
    return render_to_response('member/sukses.html','', context_instance=RequestContext(request, processors=[custom_proc]))
"""

def activation(request, key):
	emailnya = base64.urlsafe_b64decode(key.encode())
	
	user = User.objects.get(email=emailnya)
	user.is_active = True
	user.save()

	messages.success(request, "Activation Success. Please login.")
	return HttpResponseRedirect('/') 

def login_view(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect('/profil/')
	state = "Please login"
	next = ''
	if 'next' in request.GET:		
		next = request.GET['next']

	if request.POST:				# ketika submit data
		form = LoginForm(request.POST)		# isi value pada form sesuai yg di POST
		if form.is_valid():				# cek validasi
			# Data ada di array form.cleaned_data	
		        user = authenticate(
				username=form.cleaned_data['username'],
				password=form.cleaned_data['password']
			)
			if user is not None:
			    if user.is_active:
				login(request, user)								
				state = "You're successfully logged in!"
			    else:
				state = "Your account is not active, please contact the site admin."
			else:
			    state = "Your username and/or password were incorrect."

			return HttpResponseRedirect(next) 		# Redirect after POST
	else:
		form = LoginForm() 			# value form kosongan
	
	datanya = {'form': form, 'state': state, 'next': next}	
	return render_to_response('member/login.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/login/') 

@login_required
def profil(request):
	user = User.objects.get(username=request.user.username)
	profil = user.get_profile()
	gallery = Gallery.objects.select_related().filter(member=request.user)
	breadcrumb = 'Profil'

	datanya = {'profil': profil, 'gallery': gallery, 'slide_show' : False, 'breadcrumb': breadcrumb}
	return render_to_response('member/profil.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def profil_edit(request):
	user = User.objects.get(username=request.user.username)
	profil = user.get_profile()

	if request.method == 'POST':				# ketika submit data
		form = EditProfilForm(request.POST, instance=profil)		# isi value pada form sesuai yg di POST
		if form.is_valid():				# cek validasi
			# Data ada di array form.cleaned_data
			#kota = Kota.objects.get(pk=form.cleaned_data['kota'])					
			profil.nama = form.cleaned_data['nama']
			profil.alamat = form.cleaned_data['alamat']
			profil.tgl_lahir = form.cleaned_data['tgl_lahir']
			#profil.kota = kota
			#profil.propinsi = form.cleaned_data['propinsi']
			profil.no_hape = form.cleaned_data['no_hape']
			profil.gender = form.cleaned_data['gender']	
			profil.save()						#update data tambahan user ke member			

			messages.success(request, "Your Profil has been updated.")
			return HttpResponseRedirect('/profil/') 		# Redirect after POST
	else:
		form = EditProfilForm(instance=profil)		# value form kosongan

	datanya = {'profil': profil, 'form': form, 'slide_show' : False}
	return render_to_response('member/edit_profil.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))

@login_required
def profil_change_photo(request):
	user = User.objects.get(username=request.user.username)
	profil = user.get_profile()

	if request.method == 'POST':				# ketika submit data
		form = ChangePhotoForm(request.POST)		# isi value pada form sesuai yg di POST
		if form.is_valid():				# cek validasi
			if request.FILES :					
				f = request.FILES['image']			
				path = get_file_path(request,f.name)
				fd = open('%s/%s' % (settings.MEDIA_ROOT, str(path)), 'wb')
				for chunk in f.chunks():
					fd.write(chunk)
				fd.close()	
				
				profil.foto = path	
				profil.save()						#update data tambahan user ke member			

				messages.success(request, "Your Photo Profil has been updated.")
				return HttpResponseRedirect('/profil/') 		# Redirect after POST
			else:
				return HttpResponseRedirect('/profil/') 		# Redirect after POST
	else:
		form = ChangePhotoForm()		# value form kosongan

	datanya = {'profil': profil, 'form': form, 'slide_show' : False}
	return render_to_response('member/change_photo.html',datanya, context_instance=RequestContext(request, processors=[custom_proc]))
	
