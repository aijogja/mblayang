from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey
from apps.wisata.models import Propinsi, Kota
import uuid
import os

# Create your models here.
def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('foto', filename)

class Profil(models.Model):
	user = models.OneToOneField(User)
	nama = models.CharField(max_length=100, blank=True, null=True)
	alamat = models.CharField(max_length=100)
	tgl_lahir = models.DateField(null=True)
	propinsi = models.ForeignKey(Propinsi, blank=True, null=True)
	kota = ChainedForeignKey(Kota, chained_field="propinsi", chained_model_field="propinsi", blank=True, null=True)
	no_hape = models.CharField(max_length=20, blank=True, null=True)
	Gender_choise = (('L', 'Laki-Laki'),('P', 'Perempuan'))	
	gender = models.CharField(max_length=2, choices=Gender_choise, default='L')
	foto = models.FileField(upload_to=get_file_path, blank=True, null=True)
	
	class Meta:
		verbose_name_plural = "Profil"

	def __unicode__(self):
		return self.user.username

def create_profil_user_callback(sender, instance, **kwargs):
	profil, created = Profil.objects.get_or_create(user=instance)
post_save.connect(create_profil_user_callback, User)
