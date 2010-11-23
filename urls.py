# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^duygudrm/', include('duygudrm.foo.urls')),
    (r'^$',"duygudrm.ddapp.views.index"),
    (r'^live$',"duygudrm.ddapp.views.live"),
    (r'^upload$',"duygudrm.ddapp.views.upload"),
    #(r'^p/(.*)$',"duygudrm.ddapp.views.post"),
    #(r'^m/$',"duygudrm.ddapp.views.messages"),
    #(r'^m/(.*)$',"duygudrm.ddapp.views.messages"),
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^proxy$', 'duygudrm.ddapp.views.proxy'),
    (r'^imgproxy$', 'duygudrm.ddapp.views.imgproxy'),

    #(r'^logout$',"duygudrm.ddapp.views.logout"),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^statics/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'statics/'}),
    # Uncomment the next line to enable the admin:
    (r'^i18n/', include('django.conf.urls.i18n')),
    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    (r'^admin_001/', include(admin.site.urls)),
    (r'^(.*)$',"duygudrm.ddapp.views.user"),
)
