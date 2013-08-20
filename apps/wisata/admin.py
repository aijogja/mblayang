from apps.wisata.models import Wisata, Propinsi, Kota, Kategori, Comment, Like, Gallery, Laporkan
from django.contrib import admin

class KotaInline(admin.TabularInline):
    model = Kota
    extra = 1

class PropinsiAdmin(admin.ModelAdmin):
	list_display = ('nama_propinsi', 'title', 'ordinat')
	fieldsets = [
	    ('Nama Propinsi', {'fields': ['nama_propinsi']}),
	    ('Detail', {'fields': ['title', 'ordinat'], 'classes': ['collapse']}),
	]
        inlines = [KotaInline]

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
        
class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 1

class WisataAdmin(admin.ModelAdmin):
	list_display = ('nama', 'propinsi', 'kota', 'kategori')
	list_filter = ('kategori','propinsi')
	inlines = [CommentInline, LikeInline, GalleryInline]

class LaporkanAdmin(admin.ModelAdmin):
    list_display = ('user', 'wisata', 'alasan')
    list_filter = ('user','wisata')

admin.site.register(Laporkan, LaporkanAdmin)
admin.site.register(Wisata, WisataAdmin)
admin.site.register(Propinsi, PropinsiAdmin)
admin.site.register(Kategori)
