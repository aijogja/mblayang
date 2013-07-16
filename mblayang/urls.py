from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
base64_pattern = r'(?:[A-Za-z0-9+/]{4})*(?:[A-Za-z0-9+/]{2}==|[A-Za-z0-9+/]{3}=)?$'

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'mblayang.views.home', name='home'),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    # Member App

    url(r'^registration/$', 'apps.member.views.registrasi'),
    #url(r'^registration_sukses/$', 'apps.member.views.sukses'),
    url(r'^activate/(?P<key>{})'.format(base64_pattern), 'apps.member.views.activation'),
    url(r'^login/$', 'apps.member.views.login_view'),
    url(r'^logout/$', 'apps.member.views.logout_view'),
    url(r'^profil/$', 'apps.member.views.profil'),    
    url(r'^profil/edit$', 'apps.member.views.profil_edit'),
    url(r'^profil/change_picture$', 'apps.member.views.profil_change_photo'),
    # Wisata App
    url(r'^wisata/$', 'apps.wisata.views.wisata_index'),
    url(r'^wisata/all$', 'apps.wisata.views.wisata_all'),
    url(r'^wisata/add_location/$', 'apps.wisata.views.add_wisata'),
    #url(r'^wisata/wisata_sukses/$', 'apps.wisata.views.add_sukses'),    
    url(r'^wisata/(\d+)/add_galery/$', 'apps.wisata.views.add_gallery'),
    url(r'^wisata/(\d+)/$', 'apps.wisata.views.wisata_detail'),  
    url(r'^wisata/kategori/([A-Za-z]+)/$', 'apps.wisata.views.wisata_category'), 
    url(r'^ajax/like/(\d+)/$', 'apps.wisata.views.like'),
    url(r'^ajax/unlike/(\d+)/$', 'apps.wisata.views.unlike'),
    #url(r'^ajax/get_city/(\d+)/$', 'apps.wisata.views.get_city'),
    # News App 
    url(r'^news/$', 'apps.news.views.news_index'),
    url(r'^news/add_news/$', 'apps.news.views.news_add'),
    url(r'^news/all$', 'apps.news.views.news_all'),
    url(r'^news/(\d+)/$', 'apps.news.views.news_detail'),
    # Other
    url(r'^chaining/', include('smart_selects.urls')),
)

