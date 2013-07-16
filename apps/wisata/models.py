from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver
from smart_selects.db_fields import ChainedForeignKey, GroupedForeignKey
import uuid
import os

# Create your models here.
def get_file_path(instance, filename):
	ext = filename.split('.')[-1]
	filename = "%s.%s" % (uuid.uuid4(), ext)
	return os.path.join('gallery', filename)

class Kategori(models.Model):
	kategori = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)

	class Meta:
		verbose_name_plural = "Kategori"

	def __unicode__(self):
		return self.kategori

class Propinsi(models.Model):
	nama_propinsi = models.CharField(max_length=200)
	title = models.CharField(max_length=200, blank=True, null=True)
	ordinat = models.CharField(max_length=100, blank=True, null=True)

	class Meta:
		verbose_name_plural = "Propinsi"

	def __unicode__(self):
		return self.nama_propinsi

class Kota(models.Model):
	propinsi = models.ForeignKey(Propinsi)
	nama_kota = models.CharField(max_length=200)

	class Meta:
		verbose_name_plural = "Kota"

	def __unicode__(self):
		return self.nama_kota	

class Wisata(models.Model):
	nama = models.CharField(max_length=200)
	description = models.TextField(blank=True, null=True)
	location = models.CharField(max_length=100, blank=True, null=True)
	image = models.FileField(upload_to=get_file_path, blank=True, null=True)	
	kategori = models.ForeignKey(Kategori, blank=True, null=True)
	hit = models.IntegerField(blank=True, default=0)
	tanggal = models.DateField(auto_now_add=True, blank=True, null=True)
	member = models.ForeignKey(User)
	propinsi = models.ForeignKey(Propinsi, blank=True, null=True)
	kota = ChainedForeignKey(Kota, chained_field="propinsi", chained_model_field="propinsi", blank=True, null=True)

	class Meta:
		verbose_name_plural = "Wisata"

	def __unicode__(self):
		return self.nama

	#def delete(self, *args, **kwargs):
	#	if self.image :
				# You have to prepare what you need before delete the model
	#		storage, path = self.image.storage, self.image.path
				# Delete the model before the file
	#		super(Wisata, self).delete(*args, **kwargs)
				# Delete the file after the model
	#		storage.delete(path)
	#	else :
	#		super(Wisata, self).delete(*args, **kwargs)

class Gallery(models.Model):
	image = models.FileField(upload_to=get_file_path, blank=True, null=True)	
	wisata = models.ForeignKey(Wisata)
	member = models.ForeignKey(User)
	visible = models.BooleanField(max_length=5)

class Comment(models.Model):
	user = models.ForeignKey(User)
	wisata = models.ForeignKey(Wisata)
	comment = models.TextField(blank=True, null=True)
	tanggal = models.DateField(auto_now_add=True)

class Like(models.Model):
	user = models.ForeignKey(User)
	wisata = models.ForeignKey(Wisata)
	#Like_choise = (('like', 'Like'),('dislike', 'Dislike'))	
	like = models.BooleanField(max_length=10)
	
	class Meta:
		unique_together = ('user', 'wisata')
		    
@receiver(pre_delete, sender=Wisata)
def wisata_delete(sender, instance, **kwargs):
	if instance.image :
    		instance.image.delete(False)	# Pass false so FileField doesn't save the model.

