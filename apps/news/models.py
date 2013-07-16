from django.db import models
from django.contrib.auth.models import User
from apps.wisata.models import get_file_path

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(null=True)
    image = models.FileField(upload_to=get_file_path, blank=True, null=True)    
    tanggal = models.DateField(auto_now_add=True)
    member = models.ForeignKey(User)
    hit = models.IntegerField(blank=True, default=0)
    
    class Meta:
        verbose_name_plural = "News"

    def __unicode__(self):
        return self.title