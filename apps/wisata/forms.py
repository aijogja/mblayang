from django import forms
from django.contrib.auth.models import User
from django.core.validators import ValidationError
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey
from apps.wisata.models import Propinsi, Kota, Kategori

class AddWisata(forms.Form):
	nama = forms.CharField(label='Nama', max_length=200, widget=forms.TextInput(attrs={'class':'span4', 'placeholder':'Nama Tempat'}))
	description = forms.CharField(label='Deskripsi ', widget = forms.Textarea(attrs={'class':'span4'}), required=False)
	location = forms.CharField(label='Lokasi ', max_length=200, widget=forms.TextInput(attrs={'class':'span4', 'placeholder':'Latitude (ex: -7.816276,110.387878)'}), required=False)
	image = forms.FileField()
	kategori = forms.ModelChoiceField(queryset=Kategori.objects.all(), widget = forms.Select(attrs={'class':'span2'}))
	propinsi = forms.ModelChoiceField(queryset=Propinsi.objects.all(), widget = forms.Select(attrs={'class':'span2'}))
	kota = forms.ModelChoiceField(queryset=Kota.objects.all(), widget = forms.Select(attrs={'class':'span2'}))#forms.ChoiceField(widget = forms.Select(attrs={'class':'chained'}), )

	#def clean_kota(self):
	#	kota = self.cleaned_data['kota']		
	#	if kota != 3:		
	#		raise ValidationError(kota.value)		
	#	return kota	
	
class CommentForm(forms.Form):
	comment = forms.CharField(label='Comment ',  widget = forms.Textarea(attrs={'class':'span12', 'rows':3}))

class AddGallery(forms.Form):
	image = forms.FileField()
	visible = forms.BooleanField(required=False)

