from django.conf.urls.defaults import *
from django.conf import settings

# These are the site specific urls that define how access is controlled to the
# application via URL requests
urlpatterns = patterns('',
    # Example:
    (r'^$', 'duygudrm.wrap.views.index'),
    (r'^OAuthResponseHandler$', 'duygudrm.wrap.views.oauth_response_handler'),
    (r'^consent$', 'duygudrm.wrap.views.consent_redirect'),
    (r'^access$', 'duygudrm.wrap.views.access_request'),
    (r'^refresh$', 'duygudrm.wrap.views.refresh_request'),
    #This servers the static CSS files
    
)

