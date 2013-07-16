from apps.member.models import Profil
from django.contrib import admin

class ProfilAdmin(admin.ModelAdmin):
	list_display = ('user', 'nama', 'no_hape')

admin.site.register(Profil, ProfilAdmin)
