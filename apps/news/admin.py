from apps.news.models import News
from django.contrib import admin

class NewsAdmin(admin.ModelAdmin):
    list_display = ('member', 'title', 'tanggal')
    list_filter = ('member','tanggal')
    
admin.site.register(News, NewsAdmin)