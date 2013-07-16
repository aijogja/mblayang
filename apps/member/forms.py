from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from apps.wisata.models import Propinsi, Kota, Kategori
from apps.member.models import Profil

class RegistrasiForm(forms.Form):
	email = forms.EmailField(label='Email', widget = forms.TextInput(attrs={'class':'span4'}))
	username = forms.CharField(label='Username', widget = forms.TextInput(attrs={'class':'span4'}))
	password = forms.CharField(label='Password', max_length=100, widget = forms.PasswordInput(render_value=False, attrs={'class':'span4'}))
	repassword = forms.CharField(label='Verify Password', max_length=100, widget = forms.PasswordInput(render_value=False, attrs={'class':'span4'}))
	nama = forms.CharField(label='Full Name', max_length=200, widget = forms.TextInput(attrs={'class':'span4'}))
	alamat = forms.CharField(label='Address', max_length=100, widget = forms.TextInput(attrs={'class':'span4'}))
	image = forms.FileField(label='Picture', required=False)
	tgl_lahir = forms.DateField(label='Date of Birth', widget = forms.TextInput(attrs={'class':'span2 datepiker'}))
	propinsi = forms.ModelChoiceField(queryset=Propinsi.objects.all(), widget = forms.Select(attrs={'class':'span2'}))	
	kota = forms.ModelChoiceField(queryset=Kota.objects.all(), widget = forms.Select(attrs={'class':'span2'}))
	#kota = forms.CharField(label='City ', max_length=50, widget = forms.TextInput(attrs={'class':'span2'}))	
	#propinsi = forms.CharField(label='State ', max_length=50, widget = forms.TextInput(attrs={'class':'span2'}))
	no_hape = forms.CharField(label='Phone ', max_length=20, widget = forms.TextInput(attrs={'class':'span4'}), required=False)
	Gender_choise = (('L', 'Laki-Laki'),('P', 'Perempuan'))
	gender = forms.ChoiceField(label='Gender ', widget = forms.RadioSelect(), choices = Gender_choise)

	def clean_email(self):
		email = self.cleaned_data['email']		
		try:
			User.objects.get(email=email)
		except User.DoesNotExist:
			return email
		raise ValidationError("The Email already exists")

	def clean_username(self):
		username = self.cleaned_data['username']		
		try:
			User.objects.get(username=username)
		except User.DoesNotExist:
			return username
		raise ValidationError("The Username already exists")

	def clean_repassword(self):
		password = self.cleaned_data['password']	
		repassword = self.cleaned_data['repassword']
		if password != repassword:		
			raise ValidationError("The Password didn't match. Please try again")		
		return repassword

class EditProfilForm(forms.ModelForm):
	class Meta:
		model = Profil
		fields = ['nama', 'alamat', 'tgl_lahir', 'propinsi', 'kota', 'no_hape', 'gender']	

class ChangePhotoForm(forms.Form):
	image = forms.FileField(label='Picture', required=False)	

class LoginForm(forms.Form):
	username = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class':'span4', 'placeholder':'Username'}))
	password = forms.CharField(max_length=50, widget = forms.PasswordInput(render_value=False, attrs={'class':'span4', 'placeholder':'Password'}))
	

