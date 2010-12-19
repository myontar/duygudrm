from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponseBadRequest
from django.template import Context
from django.template import loader
from duygudrm.wrap.OAuthHandler import OAuthWrapHandler
from django.conf import settings

def index(request):
    
    return consent_redirect(request)

def consent_redirect(request):
    #Redirects to the Live authentication consent UX via the 'consent' URL.
    try:
        
        wrap = OAuthWrapHandler()
        wrap.wrap_urls = settings.WRAP_URLS
        wrap.app_id = settings.LIVE_APP_ID
        wrap.app_secret = settings.LIVE_APP_SECRET
        wrap.callback = settings.LIVE_DEFAULT_CALLBACK

        wrap.scope = settings.LIVE_DEFAULT_SCOPE
            
        url = wrap.build_consent_url()

        request.session['wrap'] = wrap
        response = HttpResponseRedirect(url)
    except KeyError:
        response = __redirect_on_bad_request()

    return response

def oauth_response_handler(request):
    #Callback for responses from the LIVE consent UX.
    try:
        wrap = request.session['wrap']

        if 'wrap_verification_code' in request.GET:
            wrap.verification_code = request.GET['wrap_verification_code']

        wrap.consent_response = request.GET
        request.session['wrap'] = wrap
        response = HttpResponseRedirect('/messenger/access')
    except KeyError:
        response = __redirect_on_bad_request()

    return response

def access_request(request):
    #Requests authorization tokens via the 'access' URL.
    try:
        wrap = request.session['wrap']
        #wrap.app_secret = wrap.consent_response['accessAppSecret']


        
        wrap.get_authorization_token()
        request.session['wrap'] = wrap
        request.session['userinfo'] = wrap.userdata()
        response = HttpResponseRedirect('/msnregister')
    except KeyError:
        response = __redirect_on_bad_request()

    return response

def refresh_request(request):
    #Requests refreshed authorization tokens via the 'refresh' URL.
    try:
        wrap = request.session['wrap']
        wrap.refresh_authorization_token()
        request.session['wrap'] = wrap
        response = HttpResponseRedirect('/')
    except KeyError:
        response = __redirect_on_bad_request()

    return response

def __redirect_on_bad_request():
    #Returns A Django HttpResponseBadRequest object that redirects to the
    #index page after 5 seconds.
    response = HttpResponseBadRequest("You have come to this page out of " \
        "step or have incorrectly completed a previous step. We will redirect "\
        "you to the landing page in 5 seconds.")
    response['Refresh'] = "5; url=/"

    return response
