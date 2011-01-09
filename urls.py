# -*- coding: utf-8 -*-

from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()
js_info_dict = {
    'domain':"djangojs",
    'packages': ('duygudrm.ddapp',),
}

urlpatterns = patterns('',
    # Example:
    # (r'^duygudrm/', include('duygudrm.foo.urls')),
    (r'^$',"duygudrm.ddapp.views.index"),
    (r'^live$',"duygudrm.ddapp.views.live"),
    (r'^login_yahoo$',"duygudrm.ddapp.views.loginyahoo"),
    (r'^login_linkedin$',"duygudrm.ddapp.views.login_linkedin"),
    (r'^signin_linkedin$',"duygudrm.ddapp.views.signin_linkedin"),
    (r'^privacy$',"duygudrm.ddapp.views.priv"),                  
    (r'^connect$',"duygudrm.ddapp.views.connect"),
    (r'^getAlerts$',"duygudrm.ddapp.views.getalerts"),
    (r'^getAlertsx$',"duygudrm.ddapp.views.getalertsx"),
    (r'^groups$',"duygudrm.ddapp.views.groups"),
    (r'^signin_yahoo$',"duygudrm.ddapp.views.sigyaho"),
    (r'^Oiuw1vgYCq6S2ODnX236Dz82.txt$',"duygudrm.ddapp.views.msntxt"),
    (r'^vKkb3_o3cSjWEBXYNLHxxQ--.html$',"duygudrm.ddapp.views.msntxt"),

                       
    (r'^passcountry$',"duygudrm.ddapp.views.gopass"),
    (r'^fallows$',"duygudrm.ddapp.views.ufallows"),
    (r'^fallowers$',"duygudrm.ddapp.views.ufallowers"),
    (r'^jsi18n/$', 'django.views.i18n.javascript_catalog', js_info_dict),

                  
    (r'^upload$',"duygudrm.ddapp.views.upload"),
    (r'^linkedin_clogin$',"duygudrm.ddapp.views.loginconnect_linkedin"),
    (r'^yahoo_clogin$',"duygudrm.ddapp.views.logincyahoo"),
    (r'^connect_yahoo$',"duygudrm.ddapp.views.connect_yahoo"),
    (r'^connect_linkedin$',"duygudrm.ddapp.views.connect_linkedin"),
    (r'^profile$',"duygudrm.ddapp.views.meprofile"),
    #(r'^p/(.*)$',"duygudrm.ddapp.views.post"),
    #(r'^m/$',"duygudrm.ddapp.views.messages"),
    #(r'^m/(.*)$',"duygudrm.ddapp.views.messages"),
    (r'^login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}),
    (r'^signin_facebook$', "duygudrm.ddapp.views.loginfacebook"),
    (r'^connect_facebook$', "duygudrm.ddapp.views.connectfacebook"),
    (r'^reg_facebook$', "duygudrm.ddapp.views.reg_facebook"),
    (r'^register_to_facebook$', "duygudrm.ddapp.views.register_to_facebook"),
    (r'^signin_twitter$', "duygudrm.ddapp.views.signin"),
    (r'^msnregister$', "duygudrm.ddapp.views.msnregister"),
    (r'^msnconnect$', "duygudrm.ddapp.views.msnconnect"),
    (r'^signin_friendfeed$', "duygudrm.ddapp.views.friendfeed"),
    (r'^connect_friendfeed$', "duygudrm.ddapp.views.connect_friendfeed"),
    (r'^connect_twitter$', "duygudrm.ddapp.views.connect_twitter"),
    (r'^ffauth$', "duygudrm.ddapp.views.ffauth"),
    (r'^messenger/', include('duygudrm.wrap.urls')),
    (r'^twitter_return$', "duygudrm.ddapp.views.twitterreturn"),
    (r'^comments$',"duygudrm.ddapp.views.getcommentt"),
    (r'^proxy$', 'duygudrm.ddapp.views.proxy'),
    (r'^logout$', 'duygudrm.ddapp.views.logout_view'),
    (r'^search$', 'duygudrm.ddapp.views.search'),
    (r'^imgproxy$', 'duygudrm.ddapp.views.imgproxy'),

    #(r'^logout$',"duygudrm.ddapp.views.logout"),
    (r'^avatar/(.*)$', 'duygudrm.ddapp.views.avatarControl'),
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^statics/(?P<path>.*)$', 'django.views.static.serve',{'document_root': 'statics/'}),
    (r'^(?P<path>.*).htm$', 'django.views.static.serve',{'document_root': '/'}),
    # Uncomment the next line to enable the admin:
    (r'^i18n/', include('django.conf.urls.i18n')),
    
    # Uncomment the next line to enable the admin:
    #(r'^admin/', include(admin.site.urls)),
    (r'^mn/(.*)$',"duygudrm.ddapp.views.usermini"),
    (r'^admin_001/', include(admin.site.urls)),
    (r'^s/(.*)$',"duygudrm.ddapp.views.short"),
    (r'^(.*)/comments$',"duygudrm.ddapp.views.getcomment"),
    (r'^(.*)/likes$',"duygudrm.ddapp.views.getlike"),
    (r'^(.*)/fallows$',"duygudrm.ddapp.views.fallowsx"),
    (r'^(.*)/mood$',"duygudrm.ddapp.views.moodlist"),
    (r'^(.*)/fallowers$',"duygudrm.ddapp.views.fallowersx"),
    (r'^(.*)/(.*)$',"duygudrm.ddapp.views.getsinglepost"),
    (r'^(.*)$',"duygudrm.ddapp.views.user"),
    
    
)
