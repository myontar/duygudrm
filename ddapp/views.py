# -*- coding: utf-8 -*-
'''
Created on 04.Kas.2010

@author: Administrator
'''
from django.contrib.auth import authenticate
from django.contrib.auth import  login

from duygudrm.ddapp.models import fallowers
import os.path
from django.utils.encoding import *
from duygudrm.ddapp.extras.mtoken import makeToken , controltoken
from duygudrm.ddapp.extras import linkedin
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.template import Context, loader
from django.shortcuts import render_to_response
from django.core.context_processors import request
from django.utils import translation
from django.core.context_processors import csrf
from django.contrib.csrf.middleware import csrf_exempt
from django.views.decorators.csrf import  csrf_protect
from duygudrm.ddapp.models import *
import datetime
from django.contrib.auth.decorators import login_required
import json , os ,sys
import time , StringIO
from PIL import Image
import memcache
from django.contrib.auth.models import User
from duygudrm.ddapp.models import UserProfiles , UserAlerts , sendAlert , groupowners
from oauthtwitter import OAuthApi
from duygudrm.ddapp.extras.friendfeed import *
import oauth.oauth as oauth
from django.template import RequestContext
from duygudrm.ddapp.extras.ip import controlIPL
cache = memcache.Client(['127.0.0.1:11211'])


def MakingRender(template,request=None,params={}):
    
    c = params
    template = template
    c.update(csrf(request))
    c['time'] = md()
    c['ttoken'] = makeToken(request,0)
    c['ugent'] = request.META['HTTP_USER_AGENT']
    if request.META['HTTP_USER_AGENT'].lower().find("apple") > -1:
        if request.META['HTTP_USER_AGENT'].lower().find("qt/") > -1:
            template = "qt_"+template
    logged = None
    if request.user.is_authenticated():
        logged = request.user
    c['login'] = logged
    ucontrol = controlIPL(request.META['REMOTE_ADDR'])
    c['ucontrol'] = ucontrol

    if "pass_country" in request.COOKIES:
        c['ucontrol'] = True



    
    return render_to_response(template, c, context_instance=RequestContext(request))


@csrf_exempt
def gopass(request):

    
    response = HttpResponseRedirect("/")
    if request.POST['pid'] == "developer":
        response.set_cookie("pass_country","yes",365*60*60)
    return response

@csrf_exempt
def loginyahoo(request):
    import oauth

    import yahoo.oauth, yahoo.yql, yahoo.application


    # Yahoo! OAuth Credentials - http://developer.yahoo.com/dashboard/
    YCONSUMER_KEY      = 'dj0yJmk9MnlQMlNYZkRtVHVXJmQ9WVdrOU1FVnVUREpOTkdjbWNHbzlORGsyTnpRM05EWXkmcz1jb25zdW1lcnNlY3JldCZ4PWNh'
    YCONSUMER_SECRET   = '270fac3cd355956be9060adf35f96b6287ee2944'
    YAPPLICATION_ID    = '0EnL2M4g'
    YCALLBACK_URL      = 'http://framemind.com/signin_yahoo'
    ck  = YCONSUMER_KEY
    cks = YCONSUMER_SECRET
    app = YAPPLICATION_ID
    cb  = YCALLBACK_URL



    # make public request for data oauth requests for profiles
    oauthapp = yahoo.application.OAuthApplication(consumer_key = ck, consumer_secret  = cks,application_id=app)
    req_token = oauthapp.get_request_token(YCALLBACK_URL)
    print req_token
    
    #return HttpResponse(str(req_token))
    request.session['req_token'] = str(req_token.to_string())
    
    return HttpResponseRedirect(oauthapp.get_authorization_url(req_token))
def logincyahoo(request):
    import oauth

    import yahoo.oauth, yahoo.yql, yahoo.application


    # Yahoo! OAuth Credentials - http://developer.yahoo.com/dashboard/
    YCONSUMER_KEY      = 'dj0yJmk9MnlQMlNYZkRtVHVXJmQ9WVdrOU1FVnVUREpOTkdjbWNHbzlORGsyTnpRM05EWXkmcz1jb25zdW1lcnNlY3JldCZ4PWNh'
    YCONSUMER_SECRET   = '270fac3cd355956be9060adf35f96b6287ee2944'
    YAPPLICATION_ID    = '0EnL2M4g'
    YCALLBACK_URL      = 'http://framemind.com/connect_yahoo'
    ck  = YCONSUMER_KEY
    cks = YCONSUMER_SECRET
    app = YAPPLICATION_ID
    cb  = YCALLBACK_URL



    # make public request for data oauth requests for profiles
    oauthapp = yahoo.application.OAuthApplication(consumer_key = ck, consumer_secret  = cks,application_id=app)
    req_token = oauthapp.get_request_token(YCALLBACK_URL)
    print req_token

    #return HttpResponse(str(req_token))
    request.session['req_token'] = str(req_token.to_string())

    return HttpResponseRedirect(oauthapp.get_authorization_url(req_token))


class tkn(object):
    
    secret = ""
    oauth_token = ""
    callback = ""
    oauth_expires_in = ""

@csrf_exempt
def login_linkedin(request):

    KEY = "7h7EKQN7fWF6MKHsHCp3HcviIaaK9CZ3ot5ODXA2OdGLAAT7gfuFFg2462l44SY3"
    SCR = "nA8mntGQcUAtrBSQhriB12RQypqHcE7HbutQs-bxPX4qFfoT-VDeRdlkDS-xyF4v"

    api = linkedin.LinkedIn(KEY, SCR, "http://framemind.com/signin_linkedin")
    result = api.requestToken()
    request.session['linreq'] = api.request_token
    request.session['linreqsc'] = api.request_token_secret
    return HttpResponseRedirect( api.getAuthorizeURL())

def loginconnect_linkedin(request):

    KEY = "7h7EKQN7fWF6MKHsHCp3HcviIaaK9CZ3ot5ODXA2OdGLAAT7gfuFFg2462l44SY3"
    SCR = "nA8mntGQcUAtrBSQhriB12RQypqHcE7HbutQs-bxPX4qFfoT-VDeRdlkDS-xyF4v"

    api = linkedin.LinkedIn(KEY, SCR, "http://framemind.com/connect_linkedin")
    result = api.requestToken()
    request.session['linreq'] = api.request_token
    request.session['linreqsc'] = api.request_token_secret
    return HttpResponseRedirect( api.getAuthorizeURL())


def unameControl(uname):
    while True:
        if User.objects.filter(username=uname).count() == 0:
            return uname
        else:
            uname = uname + "-" + "1"



def groups(request):
    error = 0
    sc    = 0
    if "group" in request.POST:
        if request.user.is_authenticated():



            gg = User.objects.filter(username=request.POST['group']).count()
            if gg == 0:
                u = User()
                u.username = request.POST['group']
                u.save()
                rewrite = u"%s" % request.POST['group']
            
            

                tmp = rewrite.lower().replace(u"ı","i").replace(u"ç","c").replace(u"ş","s").replace(u"ö","o").replace(u"ü","u").replace(u"ğ","g")
            #tmp = text.lower()
                re_strip = re.compile(r'[^\w\s-]')

                re_dashify = re.compile(r'[-\s]+')
                cleanup= re_strip.sub('', tmp).strip().lower()
                rewrite =  re_dashify.sub('-', cleanup)


                u2 = UserProfiles.objects.filter(user=u).get()
                u2.user = u
                u2.is_grup = 1
                u2.rewrite = rewrite
                u2.save()

                g = groupowners()
                g.grup = u2
                u3 = UserProfiles.objects.filter(user=request.user).get()
                g.owner = u3
                g.save()
                sc = 1
            else:
                error = 1

    
    if request.user.is_authenticated():
        u3 = UserProfiles.objects.filter(user=request.user).get()
        mygroups = fallowers.objects.filter(from_user = u3 , to_user__is_grup = 1 ).all()
        mygroups.query.group_by =['to_user_id']
        u4 = UserProfiles.objects.filter(is_grup=1).all()
        return MakingRender("groups.html",request,{"s":sc,"e":error,"fallows":mygroups,"groups":u4})
    else:
        return HttpResponseRedirect("/login")


def signin_linkedin(request):
    KEY = "7h7EKQN7fWF6MKHsHCp3HcviIaaK9CZ3ot5ODXA2OdGLAAT7gfuFFg2462l44SY3"
    SCR = "nA8mntGQcUAtrBSQhriB12RQypqHcE7HbutQs-bxPX4qFfoT-VDeRdlkDS-xyF4v"

    api = linkedin.LinkedIn(KEY, SCR, "http://framemind.com/signin_linkedin")

    ove = request.GET.get('oauth_verifier','')
    aa = api.accessToken(request.session['linreq'],request.session['linreqsc'],ove)

    if 1 == 1:
    #try:
        profile = api.GetProfile(fields=['first-name','last-name','id'])


        uid = profile.id
        #return HttpResponse(uid)
        name = profile.first_name
        sname = profile.last_name
        uname = profile.first_name + "-" + profile.last_name
        email = "none@none.com"
        access_token = ""

        

        pu = userLoginService.objects.filter(service_uid = uid)


        if pu.count() == 0:
                
                uname = unameControl(uname)
                u = User()
                u.username = uname
                u.first_name = name
                u.last_name = sname
                u.email     = email
                u.is_active    = True
                u.set_password('admin001')
                u.save()
                u2 = UserProfiles.objects.filter(user=u).get()
                #u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))
                u2.rewrite = uname
                u2.save()
                user = authenticate(username=uname, password='admin001')
                uys = userLoginService()
                uys.service_param = '{"uid":'+str(uid)+',"access_token":"'+str(access_token)+'"}'
                uys.service_uid = uid
                uys.service = "linkedin"
                uys.user = u2
                uys.save()
            
        else:
            u = pu.get()
            #printu.user.user_id

            userx = User.objects.filter(id=u.user.user_id).get()
            #printuserx
            userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'
            
            #account = get_account_from_hash(ux.hash)
            user = authenticate(username=userx.username,external=1)
            #printuser
            #user = ux
        #request.session
        login(request,user)
        
       
        return HttpResponse("<script>opener.document.location='/';window.close(); </script>")
    #except Exception as e:
    #    return HttpResponse("<br /><br /><br /><center><a href='/login_linkedin'>please try again...</a></center>"+str(e))

def connect_linkedin(request):
    KEY = "7h7EKQN7fWF6MKHsHCp3HcviIaaK9CZ3ot5ODXA2OdGLAAT7gfuFFg2462l44SY3"
    SCR = "nA8mntGQcUAtrBSQhriB12RQypqHcE7HbutQs-bxPX4qFfoT-VDeRdlkDS-xyF4v"

    api = linkedin.LinkedIn(KEY, SCR, "http://framemind.com/connect_linkedin")

    ove = request.GET.get('oauth_verifier','')
    aa = api.accessToken(request.session['linreq'],request.session['linreqsc'],ove)

    if 1 == 1:
    #try:
        profile = api.GetProfile(fields=['first-name','last-name','id'])
        uid = profile.id
        access_token = ""
        pu = userLoginService.objects.filter(service_uid = uid)
        if pu.count() == 0:


                u2 = UserProfiles.objects.filter(user=request.user).get()
                #u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))

                uys = userLoginService()
                uys.service_param = '{"uid":'+str(uid)+',"access_token":"'+str(access_token)+'"}'
                uys.service_uid = uid
                uys.service = "linkedin"
                uys.user = u2
                uys.save()


        

        return HttpResponse("<script>opener.document.location = opener.document.location;window.close(); </script>")
    #except Exception as e:
    #    return HttpResponse("<br /><br /><br /><center><a href='/login_linkedin'>please try again...</a></center>"+str(e))
    
 
@csrf_exempt
def sigyaho(request):
    import oauth

    import yahoo.oauth, yahoo.yql, yahoo.application


    # Yahoo! OAuth Credentials - http://developer.yahoo.com/dashboard/
    YCONSUMER_KEY      = 'dj0yJmk9MnlQMlNYZkRtVHVXJmQ9WVdrOU1FVnVUREpOTkdjbWNHbzlORGsyTnpRM05EWXkmcz1jb25zdW1lcnNlY3JldCZ4PWNh'
    YCONSUMER_SECRET   = '270fac3cd355956be9060adf35f96b6287ee2944'
    YAPPLICATION_ID    = '0EnL2M4g'
    YCALLBACK_URL      = 'http://framemind.com/signin_yahoo'
    ck  = YCONSUMER_KEY
    cks = YCONSUMER_SECRET
    app = YAPPLICATION_ID
    cb  = YCALLBACK_URL
    tokenall = yahoo.oauth.RequestToken(YCONSUMER_KEY,YCONSUMER_SECRET)
    tokenall = tokenall.from_string(request.session['req_token'])
    #token = list()
    

    
    
    oauthapp = yahoo.application.OAuthApplication( ck, cks,app,YCALLBACK_URL)
    
    data =  oauthapp.get_access_token(tokenall,request.GET['oauth_verifier'])
    #access_token = str(data)
    profile = "http://social.yahooapis.com/v1/user/%s/profile" % data.yahoo_guid
    oauthapp2 = yahoo.application.OAuthApplication( ck, cks,app,YCALLBACK_URL,data)
    profile = profile + "?access_token="
    import oauthlib.oauth
   
    guid = data.yahoo_guid
    url =  'http://social.yahooapis.com/v1/user/%s/profile' % guid
    parameters = { 'format': 'json' }
    requests = oauthlib.oauth.OAuthRequest.from_consumer_and_token(oauthapp2.consumer, token=oauthapp2.token, http_method='GET', http_url=url, parameters=parameters)
    requests.sign_request(oauthapp2.signature_method_hmac_sha1, oauthapp2.consumer, data)
    aldata = oauthapp2.client.access_resource(requests)
    data = json.loads( aldata)
    brit_date =data['profile']['birthdate'] + "/" + str(data['profile']['birthYear'])
    access_token = ""
    uname = data['profile']['nickname'].replace(" ","-")
    email = data['profile']['emails'][0]['handle']
    name  = data['profile']['givenName']
    sname = data['profile']['familyName']
    gender = 2
    if data['profile']['gender'] == "M":
        gender = 1
    uid = guid


    pu = userLoginService.objects.filter(service_uid = uid)


    if pu.count() == 0:
            u23 = User.objects.filter(email=email)
            if u23.count() > 0:
                userx = u23.get()
                userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'

                #account = get_account_from_hash(ux.hash)
                user = authenticate(username=userx.username,external=1)
                #printuser
                #user = ux
                u2 = UserProfiles.objects.filter(user=userx).get()
                uys = userLoginService()
                uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
                uys.service_uid = uid
                uys.service = "yahoo"
                uys.user = u2
                uys.save()
                login(request,user)

                return HttpResponseRedirect("/")
            
            u = User()
            u.username = uname
            u.first_name = name
            u.last_name = sname
            u.email     = email
            u.is_active    = True
            u.set_password('admin001')
            u.save()
            u2 = UserProfiles.objects.filter(user=u).get()
            u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))
            u2.rewrite = uname
            u2.save()
            user = authenticate(username=uname, password='admin001')
            uys = userLoginService()
            uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
            uys.service_uid = uid
            uys.service = "yahoo"
            uys.user = u2
            uys.save()
        
    else:
        u = pu.get()
        #printu.user.user_id

        userx = User.objects.filter(id=u.user.user_id).get()
        #printuserx
        userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'
        
        #account = get_account_from_hash(ux.hash)
        user = authenticate(username=userx.username,external=1)
        #printuser
        #user = ux
    #request.session
    login(request,user)
    
   
    return HttpResponse("<script>opener.document.location='/';window.close(); </script>")
def connect_yahoo(request):
    import oauth

    import yahoo.oauth, yahoo.yql, yahoo.application


    # Yahoo! OAuth Credentials - http://developer.yahoo.com/dashboard/
    YCONSUMER_KEY      = 'dj0yJmk9MnlQMlNYZkRtVHVXJmQ9WVdrOU1FVnVUREpOTkdjbWNHbzlORGsyTnpRM05EWXkmcz1jb25zdW1lcnNlY3JldCZ4PWNh'
    YCONSUMER_SECRET   = '270fac3cd355956be9060adf35f96b6287ee2944'
    YAPPLICATION_ID    = '0EnL2M4g'
    YCALLBACK_URL      = 'http://framemind.com/connect_yahoo'
    ck  = YCONSUMER_KEY
    cks = YCONSUMER_SECRET
    app = YAPPLICATION_ID
    cb  = YCALLBACK_URL
    tokenall = yahoo.oauth.RequestToken(YCONSUMER_KEY,YCONSUMER_SECRET)
    tokenall = tokenall.from_string(request.session['req_token'])
    #token = list()




    oauthapp = yahoo.application.OAuthApplication( ck, cks,app,YCALLBACK_URL)

    data =  oauthapp.get_access_token(tokenall,request.GET['oauth_verifier'])
    #access_token = str(data)
    profile = "http://social.yahooapis.com/v1/user/%s/profile" % data.yahoo_guid
    oauthapp2 = yahoo.application.OAuthApplication( ck, cks,app,YCALLBACK_URL,data)
    profile = profile + "?access_token="
    import oauthlib.oauth

    guid = data.yahoo_guid
    url =  'http://social.yahooapis.com/v1/user/%s/profile' % guid
    parameters = { 'format': 'json' }
    requests = oauthlib.oauth.OAuthRequest.from_consumer_and_token(oauthapp2.consumer, token=oauthapp2.token, http_method='GET', http_url=url, parameters=parameters)
    requests.sign_request(oauthapp2.signature_method_hmac_sha1, oauthapp2.consumer, data)
    aldata = oauthapp2.client.access_resource(requests)
    data = json.loads( aldata)

    access_token = ""
   
    uid = guid


    pu = userLoginService.objects.filter(service_uid = uid)


    if pu.count() == 0:

            u2 = UserProfiles.objects.filter(user=request.user).get()

            uys = userLoginService()
            uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
            uys.service_uid = uid
            uys.service = "yahoo"
            uys.user = u2
            uys.save()


    return HttpResponse("<script>opener.document.location=opener.document.location;window.close(); </script>")
    

@csrf_exempt
def gopass(request):


    response = HttpResponseRedirect("/")
    if request.POST['pid'] == "developer":
        response.set_cookie("pass_country","yes",365*60*60)
    return response

def reg_facebook(request):
    return MakingRender("regface.html",request,{})
@csrf_exempt
def register_to_facebook(request):
    a = request.REQUEST['signed_request']#.get("signed_request")
    return HttpResponse(a)
def loginfacebook(request):
    
    cokie = request.GET['token']
    cookies = {}

    access_token = cokie
    uid = request.GET['uid']

    import urllib2
    std_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.11) Gecko/20101019 Firefox/3.6.11',
            'Accept-Charset': ' ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    ##printrequest.GET['p']
    urequest = urllib2.Request("https://graph.facebook.com/me?access_token="+access_token, None, std_headers)
    video_info_webpage = urllib2.urlopen(urequest).read()

    data = json.loads(video_info_webpage)
    gender = 2
    if data['gender'] == "male":
        gender = 1

    brit_date  = data['birthday']
    name       = data['name']
    last_name  = data['last_name']
    first_name = data['first_name']
    locale     = data['locale']
    email     = data['email']

    pu = userLoginService.objects.filter(service_uid = uid)


    if pu.count() == 0:
            u23 = User.objects.filter(email=email)
            if u23.count() > 0:
                userx = u23.get()
                userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'

                #account = get_account_from_hash(ux.hash)
                user = authenticate(username=userx.username,external=1)
                #printuser
                #user = ux
                u2 = UserProfiles.objects.filter(user=userx).get()
                uys = userLoginService()
                uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
                uys.service_uid = uid
                uys.user = u2
                uys.service = "facebook"
                uys.save()
                login(request,user)

                return HttpResponseRedirect("/")
            
            u = User()
            u.username = first_name+"_"+last_name
            u.first_name = first_name
            u.last_name = last_name
            u.email     = email
            u.is_active    = True
            u.set_password('admin001')
            u.save()
            u2 = UserProfiles.objects.filter(user=u).get()
            u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))
            u2.rewrite = first_name+"_"+last_name
            u2.save()
            user = authenticate(username=first_name+"_"+last_name, password='admin001')
            uys = userLoginService()
            uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
            uys.service_uid = uid
            uys.service = "facebook"
            uys.user = u2
            uys.save()
        
    else:
        u = pu.get()
        #printu.user.user_id

        userx = User.objects.filter(id=u.user.user_id).get()
        #printuserx
        userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'
        
        #account = get_account_from_hash(ux.hash)
        user = authenticate(username=userx.username,external=1)
        #printuser
        #user = ux
    #request.session
    login(request,user)
    
    return HttpResponseRedirect("/")
def connectfacebook(request):

    cokie = request.GET['token']
    cookies = {}

    access_token = cokie
    uid = request.GET['uid']

    import urllib2
    std_headers = {
            'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.11) Gecko/20101019 Firefox/3.6.11',
            'Accept-Charset': ' ISO-8859-1,utf-8;q=0.7,*;q=0.7',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
        }
    ##printrequest.GET['p']
    urequest = urllib2.Request("https://graph.facebook.com/me?access_token="+access_token, None, std_headers)
    video_info_webpage = urllib2.urlopen(urequest).read()

    data = json.loads(video_info_webpage)
    gender = 2
    if data['gender'] == "male":
        gender = 1

    brit_date  = data['birthday']
    name       = data['name']
    last_name  = data['last_name']
    first_name = data['first_name']
    locale     = data['locale']
    email     = data['email']

    pu = userLoginService.objects.filter(service_uid = uid)


    if pu.count() == 0:


            u2 = UserProfiles.objects.filter(user=request.user).get()

            uys = userLoginService()
            uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
            uys.service_uid = uid
            uys.service = "facebook"
            uys.user = u2
            uys.save()

   
    return HttpResponseRedirect("/connect")
def msnregister(request):

    cokie = request.session['userinfo']

    #brit_date  = data['birthday']
    name       = cokie['name']+ "-"  + cokie['surname']
    last_name  = cokie['surname']
    first_name = cokie['name']
    email     = cokie['mail']
    uid     = cokie['uid']
    access_token = ''
    pu = userLoginService.objects.filter(service_uid = uid)


    if pu.count() == 0:
            u23 = User.objects.filter(email=email)
            if u23.count() > 0:
                userx = u23.get()
                userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'

                #account = get_account_from_hash(ux.hash)
                user = authenticate(username=userx.username,external=1)
                #printuser
                #user = ux
                u2 = UserProfiles.objects.filter(user=userx).get()
                uys = userLoginService()
                uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
                uys.service_uid = uid
                uys.service = "msn"
                uys.user = u2
                uys.save()

            #request.session
                login(request,user)

                return HttpResponse("<script>opener.document.location='/';window.close(); </script>")
        #try:
            u = User()
            u.username = first_name+""+last_name
            u.first_name = first_name
            u.last_name = last_name
            u.email     = email
            u.is_active    = True
            u.set_password('admin001')
            u.save()
            u2 = UserProfiles.objects.filter(user=u).get()
            #u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))
            u2.rewrite = first_name+"_"+last_name
            u2.save()
            user = authenticate(username=first_name+""+last_name, password='admin001')
            uys = userLoginService()
            uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
            uys.service_uid = uid
            uys.service = "msn"
            uys.user = u2
            uys.save()

    else:
        u = pu.get()
        #printu.user.user_id

        userx = User.objects.filter(id=u.user.user_id).get()
        #printuserx
        userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'

        #account = get_account_from_hash(ux.hash)
        user = authenticate(username=userx.username,external=1)
        #printuser
        #user = ux
    #request.session
    login(request,user)

    return HttpResponse("<script>opener.document.location='/';window.close(); </script>")

def msnconnect(request):

    cokie = request.session['userinfo']

    #brit_date  = data['birthday']

    uid     = cokie['uid']
    access_token = ''
    pu = userLoginService.objects.filter(service_uid = uid)


    if pu.count() == 0:

            u2 = UserProfiles.objects.filter(user=request.user).get()
            #u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))

            uys = userLoginService()
            uys.service_param = '{"uid":'+uid+',"access_token":"'+access_token+'"}'
            uys.service_uid = uid
            uys.service = "msn"
            uys.user = u2
            uys.save()



    return HttpResponse("<script>opener.document.location=opener.document.location;window.close(); </script>")


def twitterreturn(request):
	request_token = request.session.get('request_token', None)

	# If there is no request_token for session,
	#    means we didn't redirect user to twitter
	if not request_token:
		# Redirect the user to the login page,
		# So the user can click on the sign-in with twitter button
		return HttpResponse("We didn't redirect you to twitter...")

	token = oauth.OAuthToken.from_string(request_token)
        access_token = ""
	# If the token from session and token from twitter does not match
	#   means something bad happened to tokens
	if token.key != request.GET.get('oauth_token', 'no-token'):
		del request.session['request_token']
		# Redirect the user to the login page
		return HttpResponse("Something wrong! Tokens do not match...")
        try:
            twitter = OAuthApi("AJHPnBap3l0WzRtYAtDT8g", "Bs9t4xrIjz10in0NiYUCqPbnjPwYNcsXwYjKjSN9iQw",token)
            access_token = twitter.getAccessToken()
        except Exception as e:
            print e
            pass

	#request.session['access_token'] = access_token.to_string()
	#auth_user = authenticate(access_token=access_token)

	# if user is authenticated then login user
	#if auth_user:
	#	login(request, auth_user)
	#else:
		# We were not able to authenticate user
		# Redirect to login page
	#	del request.session['access_token']
    	#	del request.session['request_token']
	#	return HttpResponse("Unable to authenticate you!")
        print access_token
        try:
            twitter = OAuthApi("AJHPnBap3l0WzRtYAtDT8g", "Bs9t4xrIjz10in0NiYUCqPbnjPwYNcsXwYjKjSN9iQw", access_token)
            userinfo = twitter.GetUserInfo()
            import json
            data = userinfo
            data =  json.loads(str(data))
            uid = str(data['id'])
        except:
            pass

        if "connect" in request.session:
                u2 = UserProfiles.objects.filter(user=request.user).get()


                uys = userLoginService()
                uys.service_param = '{"uid":'+uid+',"access_token":"'+str(access_token)+'"}'
                uys.service_uid = uid
                uys.user = u2
                uys.service = "twitter"
                uys.save()
                return HttpResponseRedirect("/connect")
        try:
            print access_token
           
            username = str(data['screen_name'])
            first_name = str(data['screen_name'])
            last_name = ""
            email = 'none@none.com'

            print uid
            print username
            #access_token = ""
            pu = userLoginService.objects.filter(service_uid = uid)
            if pu.count() == 0:
                
                u = User()
                u.username = username
                u.first_name = first_name
                u.last_name = last_name
                u.email     = email
                u.is_active    = True
                u.set_password('admin001')
                u.save()
                u2 = UserProfiles.objects.filter(user=u).get()
                #u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))
                u2.rewrite = first_name
                u2.save()
                user = authenticate(username=first_name+""+last_name, password='admin001')
                uys = userLoginService()
                uys.service_param = '{"uid":'+uid+',"access_token":"'+str(access_token)+'"}'
                uys.service_uid = uid
                uys.user = u2
                uys.service = "twitter"
                uys.save()

            else:
                u = pu.get()
                #printu.user.user_id

                userx = User.objects.filter(id=u.user.user_id).get()
                #printuserx
                userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'

                #account = get_account_from_hash(ux.hash)
                user = authenticate(username=userx.username,external=1)
                #printuser
                #user = ux
            #request.session
            login(request,user)

            return HttpResponseRedirect("/")
        except Exception as e:
            print e
            pass
            # If we cannot get the user information, user cannot be authenticated
            #print"asdasd asd asd "
	# authentication was successful, use is now logged in
	return HttpResponseRedirect("/")
def msntxt(request):
	return HttpResponse("Mu925J6SBdmClSEpaWjPEGFFaK/KeZPxQrFI+XBbRr4=")



def fallowersx(request,x):
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass



        uname = request.path.replace("/","")
        u = UserProfiles.objects.filter(rewrite=x).get()
        return MakingRender("fallower.html",request,{'user':u,"me":u2})

def ufallowers(request):
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass




        return MakingRender("fallower.html",request,{'user':u2,"me":u2})

    
def priv(request):
    if request.user.is_authenticated():
        u2 = None
        msgSave = 0
        try:
            
                
            u2 = perms.objects.filter(user=request.user)
            if u2.count() == 0:
                u2 = perms()
                u2.user = UserProfiles.objects.filter(user=request.user).get()
                u2.save()
                u2 = perms.objects.filter(user=request.user).get()
            else:
                u2 = u2.get()

            if "cmd" in request.POST:
                u2.cmd = request.POST['cmd']
                u2.freq = request.POST['freq']
                u2.feed = request.POST['feed']
                u2.dim = request.POST['dim']
                u2.postit = request.POST['postit']
                u2.save()
                msgSave = 1
                perm = cache.get("perms")
                u2 = perms.objects.filter(user=request.user).get()
                pp = {'dim':u2.dim,'cmd':u2.cmd,"feed":u2.feed,"postit":u2.postit}
                perm["%s" % str(request.user)] = json.dumps(pp)

                cache.set("perms",perm,360000)

        except Exception as e:
            return HttpResponse(str(e))
        return MakingRender("perms.html",request,{"me":u2,"msgSave":msgSave})
    else:
        return HttpResponseRedirect("/login")
def getalertsx(request):
    u = UserProfiles.objects.filter(user=request.user).get()
    ss = UserAlerts.objects.filter(user=u).all()
    for i in ss:

        i.read = 1
        i.save()
    return HttpResponse("ok")

def getalerts(request):
    u = UserProfiles.objects.filter(user=request.user).get()

    aa = UserAlerts.objects.raw(""" SELECT
ddapp_status.text,
ddapp_status.rewrite,
auth_user.username,
ddapp_useralerts.type,
ddapp_useralerts.`read`,
ddapp_userprofiles.rewrite as rew,
ddapp_useralerts.id as pk,
ddapp_useralerts.id
FROM
ddapp_status
INNER JOIN ddapp_useralerts ON ddapp_status.id = ddapp_useralerts.post_id
INNER JOIN auth_user ON auth_user.id = ddapp_useralerts.from_user
INNER JOIN ddapp_userprofiles ON ddapp_userprofiles.id = ddapp_status.from_user_id
where ddapp_useralerts.user_id = %s and ddapp_useralerts.read = 0 and (ddapp_useralerts.type = 2 or ddapp_useralerts.type = 4  or ddapp_useralerts.type = 6)
""" % u.id)
    ment = UserAlerts.objects.raw(""" SELECT
ddapp_status.text,
ddapp_status.rewrite,
auth_user.username,
ddapp_useralerts.type,
ddapp_useralerts.`read`,
ddapp_userprofiles.rewrite as rew,
ddapp_useralerts.id as pk,
ddapp_useralerts.id
FROM
ddapp_status
INNER JOIN ddapp_useralerts ON ddapp_status.id = ddapp_useralerts.post_id
INNER JOIN auth_user ON auth_user.id = ddapp_useralerts.from_user
INNER JOIN ddapp_userprofiles ON ddapp_userprofiles.id = ddapp_status.from_user_id
where ddapp_useralerts.user_id = %s and ddapp_useralerts.read = 0 and ddapp_useralerts.type = 1
""" % u.id)
    fri = UserAlerts.objects.raw(""" SELECT
auth_user.username,
ddapp_useralerts.type,
ddapp_useralerts.`read`,
ddapp_useralerts.id AS pk,
ddapp_useralerts.id
FROM
ddapp_useralerts
INNER JOIN auth_user ON auth_user.id = ddapp_useralerts.from_user
where ddapp_useralerts.user_id = %s and ddapp_useralerts.read = 0 and (ddapp_useralerts.type = 8 or ddapp_useralerts.type = 9)
 """ %  u.id)
    data = {'user':u,"alerts":aa,"ment":ment,"fri":fri}
    

    return MakingRender("alerts.html",request,data)
    

def fallowsx(request,x):
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass



        uname = request.path.replace("/","")
        u = UserProfiles.objects.filter(rewrite=x).get()
        return MakingRender("fallows.html",request,{'user':u,"me":u2})

def ufallows(request):
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass




        return MakingRender("fallows.html",request,{'user':u2,"me":u2})

def friendfeed(request):
        FRIENDFEED_API_TOKEN = dict(
                                key="ebeb6de3c71042b89da4ba2eda9c929e",
                                secret="615f26dd9d534dc88bd3913f3d704a47412d9640c1954f17bc1ca1b4944fb75b"
                            )
        facelogin = fetch_oauth_request_token(FRIENDFEED_API_TOKEN)
        ##printfacelogin
        ##printfacelogin["key"]
        data = "|".join([facelogin["key"], facelogin["secret"]])

        #cookieutil = LilCookies(self.parent
        #                                        , "kaiytbluewyth8ceywpbtdrskcutcoatlceutlbueatbice")
        #cookieutil.set_cookie(name = 'FF_API_REQ_A', value = data, expires_days= 365*100)
        request.session['FF_API_REQ_A'] = data
        fflogin_url = get_oauth_authentication_url(facelogin)
        return  HttpResponseRedirect(fflogin_url)


def connect_friendfeed(request):
    request.session['connect'] = 1
    return HttpResponseRedirect("/signin_friendfeed")
def connect_twitter(request):
    request.session['connect'] = 1
    return HttpResponseRedirect("/signin_twitter")


def connect(request):
    if request.user.is_authenticated():
        u = 1
        u2 = UserProfiles.objects.filter(user=request.user).get()
        data = userLoginService.objects.raw(" select service , id , id as pk from ddapp_userloginservice where user_id = %s group by service " % u2.id )
        dd = {}
        dd['facebook'] = 0
        dd['twitter'] = 0
        dd['friendfeed'] = 0
        dd['linkedin'] = 0
        dd['yahoo'] = 0
        dd['msn'] = 0

        for i in data:
            dd['%s' % i.service] = 1

        return MakingRender("connect.html",request,{'service':dd,"user":u2})

        

    return ""
def ffauth(request):
    ar = request
    FRIENDFEED_API_TOKEN = dict(
                            key="ebeb6de3c71042b89da4ba2eda9c929e",
                            secret="615f26dd9d534dc88bd3913f3d704a47412d9640c1954f17bc1ca1b4944fb75b",
                        )
    #if self.parent.get("oauth_token"):
    #cookieutil = LilCookies(self.parent
    #                        , "kaiytbluewyth8ceywpbtdrskcutcoatlceutlbueatbice")
    #set_cookie(self.parent.response,"Login","FF|%s" % self.parent.request.get("oauth_token"))
    request_key = request.GET["oauth_token"]
    cookie_val = request.session['FF_API_REQ_A'] #self.parent.request.cookies.get("")
    cookie_key, cookie_secret = cookie_val.split("|")
    if cookie_key != request_key:
        #logging.warning("Request token does not match cookie")
        #self.redirect("/")
        return  HttpResponse("err1")
    req_token = dict(key=cookie_key, secret=cookie_secret)
    #try:
    access_token = fetch_oauth_access_token(
        FRIENDFEED_API_TOKEN, req_token)
    datax = "|".join(access_token[k] for k in ["key", "secret", "username"])
    key, secret, username = datax.split("|")
    feed = FriendFeed(
            FRIENDFEED_API_TOKEN, dict(key=key, secret=secret))
    #self.friendfeed_username = username
    data = feed.fetch_feed_info(username)

    uid = data['id']
    first_name = data['name']
    username = data['name']
    last_name = ''
    email = 'none@none.com'
    if "connect" in request.session:
        u2 = UserProfiles.objects.filter(user=request.user).get()
        #u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))

        user = authenticate(username=first_name+""+last_name, password='admin001')
        uys = userLoginService()
        uys.service_param = '{"uid":'+uid+',"access_token":"'+str(access_token)+'"}'
        uys.service_uid = uid
        uys.service = "friendfeed"
        uys.user = u2
        uys.save()
        return HttpResponseRedirect("/connect")
    pu = userLoginService.objects.filter(service_uid = uid)
    if pu.count() == 0:

        u = User()
        u.username = username
        u.first_name = first_name
        u.last_name = last_name
        u.email     = email
        u.is_active    = True
        u.set_password('admin001')
        u.save()
        u2 = UserProfiles.objects.filter(user=u).get()
        #u2.britdate = int(time.mktime((int(brit_date.split("/")[2]),int(brit_date.split("/")[1]), int(brit_date.split("/")[0]), 0 , 0 , 0,0,0,0)))
        u2.rewrite = first_name
        u2.save()
        user = authenticate(username=first_name+""+last_name, password='admin001')
        uys = userLoginService()
        uys.service_param = '{"uid":'+uid+',"access_token":"'+str(access_token)+'"}'
        uys.service_uid = uid
        uys.service = "friendfeed"
        uys.user = u2
        uys.save()

    else:
        u = pu.get()
        #printu.user.user_id

        userx = User.objects.filter(id=u.user.user_id).get()
        #printuserx
        userx.backend = 'duygudrm.ddapp.models.MyLoginBackend'

        #account = get_account_from_hash(ux.hash)
        user = authenticate(username=userx.username,external=1)
        #printuser
        #user = ux
    #request.session
    login(request,user)

    return HttpResponseRedirect("/")



    return HttpResponse(str(data))


    #ar.sesion['friendfeed_sessions'] = "{'key':'"+key+"','secret':'"+secret+"','username':'"+username+"'}";
    #ar.sesion['friendfeed_data'] = data;
    #a:

    #    return "err2"
    # @TODO : Burası yapılması lazım
    return HttpResponseRedirect("/registerask")

def signin(request):
	twitter = OAuthApi("AJHPnBap3l0WzRtYAtDT8g", "Bs9t4xrIjz10in0NiYUCqPbnjPwYNcsXwYjKjSN9iQw")
	request_token = twitter.getRequestToken()
	request.session['request_token'] = request_token.to_string()
	signin_url = twitter.getSigninURL(request_token)
	return HttpResponseRedirect(signin_url)


def md():
    #printdatetime
    try:
        dd = datetime.datetime.now()
    except:
        pass
        #print"eeeeee"
    return time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
def scale_dimensions(width, height, longest_side):
    if width > height:
        if width > longest_side:
            ratio = longest_side*1./width
            return (int(width*ratio), int(height*ratio))
        elif height > longest_side:
            ratio = longest_side*1./height
            return (int(width*ratio), int(height*ratio))
        return (width, height)
def thumbnail(filename, size=(120, 120), output_filename=None):
    image = Image.open(filename)
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
    x,y = image.size

    perc = 0
    print x
    print y
    print filename
    if x != y:
        if x > y:
            perc = 120 / (y / 100)
            y = 120
            x = (x/100) * perc
        else:
            perc = 120 / (x / 100)
            x = 120
            y = (y/100) * perc
        size = (x,y)
    x,y = size
    image = image.resize(size, Image.ANTIALIAS)
    if x != y:
        if x > y:
            print x
            x = (x - 120) / 2
            image = image.crop((x,0,120+x,120))
        else:
            y = (y - 120) / 2
            image = image.crop((0,y,120,120+y))
    print image.size
    print x , y
    # get the thumbnail data in memory.
    if not output_filename:
        output_filename = filename
    image.save(output_filename, "JPEG")
    return output_filename

def handle_uploaded_file2(f):
    #printf.name
    destination = open('statics/users/'+f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    #i = open('statics/images/users/'+id+"_"+f.name, 'r')
    #imagefile  = StringIO.StringIO(i.read())
   
    
    return f.name


def handle_uploaded_file(f,username):
    #printf.name
    #print'statics/users/avatar/'+username
    e = ""
    if os.path.exists('/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/main_'+username+"."+e):
        os.remove('/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/main_'+username+"."+e)
        os.remove('/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/'+username+".jpg")
    
    e = str(f.name).split(".")[len(str(f.name).split("."))-1]
#print'statics/users/avatar/'+username+"."+e
    e = e.lower()
    destination = open('/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/main_'+username+"."+e, 'ab+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    #i = open('statics/images/users/'+id+"_"+f.name, 'r')
    #imagefile  = StringIO.StringIO(i.read())
   
    #print"geldik"
    thumbnail('/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/main_'+username+"."+e,(120,120),'/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/'+username+".jpg")
    os.remove('/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/main_'+username+"."+e)
    
    return '/home/django/duygudrm/statics/users/avatar/'+username
def short(request,s):
    k = shorturi.objects.filter(short=s).get()
    return HttpResponseRedirect("/"+str(k.user)+"/"+str(k.post))

def live(request):
    u = 0
    u2 = None
    if request.user.is_authenticated():
       u = 1
       u2 = UserProfiles.objects.filter(user=request.user).get()
    
    
    html = cache.get("live_html_%d" % u)
    html = None
    ##printhtml
    #return HttpResponse(str(html))
    if html == None:
        
        html = getLive(0,u,u2)
        ##printhtml
        cache.set("live_html_%d" % u,html,3600)
    
    return MakingRender("live.html",request,{'user':u2,"isuser":u,"html":html})
    
def getsinglepost(request,x,y):
    z = Status.objects.filter(from_user__user__username=x,rewrite=y).get()
    asx = []
    u2 = None
    x2 = z.from_user
    if request.user.is_authenticated():
       u = 1
       u2 = UserProfiles.objects.filter(user=request.user).get()
    u = {"id":z.id,"rewrite":z.rewrite,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
            ###printz.post
            #u.update('user',z.from_user})
            # u.user = z.from_user

    asx.append(u)
    #printasx
    return MakingRender("profile_1.html",request,{'me':u2,"user":x2,'post':asx})

def getcomment(request,x):
    z = UserProfiles.objects.filter(user__username=x).get()
    asx = []
    u2 = None
    x2 = z
    if request.user.is_authenticated():
       u = 1
       u2 = UserProfiles.objects.filter(user=request.user).get()
    u = list_comments(x,request)
            ###printz.post
            #u.update('user',z.from_user})
            # u.user = z.from_user

    asx = u
    print asx
    #printasx
    return MakingRender("profile_1.html",request,{'me':u2,"user":x2,'post':asx})

def getcommentt(request):
    
    if request.user.is_authenticated():
        u = 1
        u2 = UserProfiles.objects.filter(user=request.user).get()
        u = list_comments(u2.user.username,request)
            ###printz.post
            #u.update('user',z.from_user})
            # u.user = z.from_user

        asx = u
        print asx
        #printasx
        return MakingRender("profile_1.html",request,{'me':u2,"user":u2,'post':asx})
    return HttpResponseRedirect("/")



def getlike(request,x):
    z = UserProfiles.objects.filter(user__username=x).get()
    asx = []
    u2 = None
    x2 = z
    if request.user.is_authenticated():
       u = 1
       u2 = UserProfiles.objects.filter(user=request.user).get()
    u = list_likes(x,request)
            ###printz.post
            #u.update('user',z.from_user})
            # u.user = z.from_user

    asx = u
    print asx
    #printasx
    return MakingRender("profile_1.html",request,{'me':u2,"user":x2,'post':asx})




def search(request):

    if "q" in request.GET:
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass
        
        myStatusList = msearch(request.GET['q'],u2,request)
        return MakingRender("search.html",request,{'user':u2,'myStatusList':myStatusList[0]})
def user(request,x):
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass
        if 'file' in request.FILES:
            handle_uploaded_file(request.FILES['file'],str(request.user))
            return HttpResponseRedirect("/"+str(u2.rewrite))
            

        uname = request.path.replace("/","")
        u = UserProfiles.objects.filter(rewrite=x).get()
        postits = postit.objects.filter(user=u).all()
        return MakingRender("profile.html",request,{'user':u,"stat":u.getStat(),"me":u2,"postit":postits})
        #return MakingRender("profile.html",request)
def meprofile(request):
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass
        if 'file' in request.FILES:
            handle_uploaded_file(request.FILES['file'],str(request.user))
            return HttpResponseRedirect("/"+str(u2.rewrite))


       
        
        postits = postit.objects.filter(user=u2).all()
        return MakingRender("profile.html",request,{'user':u2,"stat":u2.getStat(),"me":u2,"postit":postits})
        #return MakingRender("profile.html",request)

def moodlist(request,x):
        u2 = None
        try:
            u2 = UserProfiles.objects.filter(user=request.user).get()
        except:
            pass
        if 'file' in request.FILES:
            handle_uploaded_file(request.FILES['file'],str(request.user))
            return HttpResponseRedirect("/"+str(u2.rewrite))


        uname = request.path.replace("/","")
        u = UserProfiles.objects.filter(rewrite=x).get()
        #postits = postit.objects.filter(user=u).all()
        return MakingRender("mood.html",request,{'user':u,"me":u2})
        #return MakingRender("profile.html",request)

def usermini(request,x):
       
        u = UserProfiles.objects.filter(rewrite=x).get()
        
        return MakingRender("profile_2.html",request,{'user':u})
        #return MakingRender("profile.html",request)


@csrf_exempt
def upload(request):
    import hashlib 
    try:
        h = request.GET['hash']
        #try:
        z = hashlib.md5()
        z.update(h)
        h = z.hexdigest()
        h = str(h)
        for k in request.FILES:
            print k
        #except:
        file = handle_uploaded_file2(request.FILES['Filedata'])
        data = cache.get(h)
        if data !=None:
            data = json.load(data)
        else:
            data = []
        data.append(file)
        cache.delete( h)
        #data = json.dump(data)
        cache.set(h,data,600)
        #print"############################ upload ok"
    except Exception as inst:
            pass
            #printtype(inst)
            #print str(inst)
            
    return HttpResponse("dememe")




def proxy(request):
    import hashlib 
    h = request.GET['p']
    z = hashlib.md5()
    z.update(h)
    h = z.hexdigest()
    
    if os.path.exists("/home/django/duygudrm/statics/proxy/"+h):
    #    return HttpResponse(open("/home/django/duygudrm/statics/proxy/"+h,"rb").read())
    #else:
        import urllib2 , urllib
        std_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.11) Gecko/20101019 Firefox/3.6.11',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        #printrequest.GET['p']
        print urllib.unquote_plus(request.GET['p'])
        request = urllib2.Request(urllib.unquote_plus(request.GET['p']), None, std_headers)
        video_info_webpage = urllib2.urlopen(request).read()
        f = open("/home/django/duygudrm/statics/proxy/"+h,"a+")
        f.write(video_info_webpage.encode("utf-8"))
        f.close()
        return HttpResponse(video_info_webpage)
def imgproxy(request):
    import hashlib 
    h = request.GET['p']
    z = hashlib.md5()
    z.update(h)
    h = z.hexdigest()
    
    if os.path.exists("/home/django/duygudrm/statics/imgproxy/"+h):
        return HttpResponse(open("/home/django/duygudrm/statics/imgproxy/"+h,"rb").read())
    else:
        import urllib2
        std_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.11) Gecko/20101019 Firefox/3.6.11',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        #printrequest.GET['p']
        request = urllib2.Request(request.GET['p'], None, std_headers)
        video_info_webpage = urllib2.urlopen(request).read()
        f = open("/home/django/duygudrm/statics/imgproxy/"+h,"a+")
        f.write(video_info_webpage)
        f.close()
        thumbnail("/home/django/duygudrm/statics/imgproxy/"+h)
        f = open("/home/django/duygudrm/statics/imgproxy/"+h,"rb").read()
        return HttpResponse(f)



def avatarControl(request,avat):
    if os.path.exists("/var/ftp/virtual_users/framemind/http/duygudrm/statics/users/avatar/"+avat):
        return HttpResponseRedirect("/statics/users/avatar/"+avat)
    else:
        return HttpResponseRedirect("/statics/users/avatar/default.jpg")
@csrf_protect 
def index(request):

    #if request.META['HTTP_HOST'] != "framemind.com":
    #    return HttpResponseRedirect("http://framemind.com")

    request.encoding = 'utf-8'
    if not request.user.is_authenticated():
        return MakingRender("index.html",request)
    else:
        
        if len(request.POST) > 0:
            u = UserProfiles.objects.filter(user=request.user).get()
            try:
                if controltoken(request) != 1:
                    
                    #response =  HttpResponse(json.dumps({'response':'err','oi':'poi',"token":""}))
                    #response.set_cookie("token",makeToken(request,0),365)
                    #printresponse
                    #return response
                    pass

                if 't' in request.POST:
                    t = request.POST['t']
                    #printmd(),t

                    all = []
                    try:
                        all = getLastest(t,u,request)
                    except:
                        #print"err"
                        pass
                    
                    #if len(all) == 0:
                    #    all = None
                    ##printall

                    try:
                        ix = UserAlerts.objects.raw(""" SELECT COUNT(*) as count , ddapp_useralerts.id , ddapp_useralerts.id as pk from ddapp_useralerts  where ddapp_useralerts.user_id = %s and ddapp_useralerts.read = 0 """ % str(u.user.id))
                        count = 0
                        for i in ix:
                            
                            count = i.count
                        
                        k = {'time':md(),"result":all[0],"token":all[1],"alerts":count}

                    except Exception as e:
                        return HttpResponse(e)
                    
                    #print"##############################"
                    #printjson.dumps(k)

                    response =  HttpResponse(json.dumps(k))
                    response.set_cookie("token",makeToken(request,0))
                    return response

            except:
                pass
            if 'postitdel' in request.POST:
                if request.user.is_authenticated():
                       referer = request.META.get('HTTP_REFERER', '')
                       if referer != '':
                           ux = referer.split("/")[-1]
                           uto = UserProfiles.objects.filter(user__username=ux).get()
                           p = postit(user=uto,to_user=u,id=request.POST['postitdel']).delete()
            if 'fallow' in request.POST:

                ux = UserProfiles.objects.filter(user__username=request.POST['fallow']).get()
                a = fallowers()
                a.from_user = u
                a.to_user = ux
                sendAlert(ux.user.username,9,0,u.user.id)
                a.save()
                return HttpResponse("ok")


            if 'unfallow' in request.POST:

                ux = UserProfiles.objects.filter(user__username=request.POST['unfallow']).get()
                a = fallowers.objects.filter(from_user = u,to_user = ux).get()
                a.delete()
                sendAlert(ux.user.username,8,0,u.user.id)
                return HttpResponse("ok")



            if 'postit' in request.POST:
                if request.user.is_authenticated():
                       referer = request.META.get('HTTP_REFERER', '')
                       if referer != '':
                           ux = referer.split("/")[-1]
                           uto = UserProfiles.objects.filter(user__username=ux).get()
                           p = postit()
                           p.user = uto
                           p.to_user = u
                           p.text = request.POST['postit']
                           p.coord = request.POST['coord']
                           if uto == u:
                               p.onay = 1
                           else:
                               p.onay = 0
                           p.save()
                           k = {'token':makeToken(request,1),"ok":1}
                           response =  HttpResponse(json.dumps(k))
                           response.set_cookie("token",makeToken(request,0))
                           return response
                        


            if 'nmode' in request.POST:
                if 'livelast' in request.POST:


                    us = 0
                    u2s = None
                    if request.user.is_authenticated():
                       us = 1
                       

                    html = getLastPost(us,u,request.POST['livelast'].replace("p_",""))
                    return HttpResponse(json.dumps(html))
            if 'getU' in request.POST:
                try:
                    rep = request.POST['getU'].lower()

                    s = UserProfiles.objects.filter(rewrite__contains=rep).all()[:20]
                    r = list()
                    r.append({'id':"all",'name':"Herkese"})
                    for i in s:
                        r.append({'id':i.rewrite,'name':str(i.user)})

                    return HttpResponse(json.dumps(r))

                except Exception as inst:
                    pass
                    #printtype(inst)
                #return HttpResponse( str(inst))
            if 'rc' in request.POST:
                s = Status.objects.filter(id=request.POST['id']).get()
                
                s.deleteComment(request.POST['rc'],u)
                response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response
            
            if 'hc' in request.POST:
                s = Status.objects.filter(id=request.POST['id']).get()

                s.hideComment(request.POST['hc'],u)
                response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response
            if 'ehc' in request.POST:
                s = Status.objects.filter(id=request.POST['id']).get()

                s.showComment(request.POST['ehc'],u)
                response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response

            if 'ec' in request.POST:
                s = Status.objects.filter(id=request.POST['id']).get()
                
                s.editComment(request.POST['ec'],u,request.POST['text'])
                response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response

            if 'rppost' in request.POST:
                s = Status.objects.filter(id=request.POST['rppost']).get()
                
                s.report(u)
                response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response


            if 'dpost' in request.POST:
                s = Status.objects.filter(id=request.POST['dpost'],from_user = u).get()
                
                s.postDelete()
                response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response
                
              
            if 'reply' in request.POST:
                try:
                    reply = request.POST['reply'].replace("p_","")
                    s = Status.objects.filter(id=reply).get()
                    s.last_update = md()
                    s.save(0)
                    u.user_comments = u.user_comments + 1
                    u.save()
                    s.saveComment(u,request.POST['text'],md())
                    

                    response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                    response.set_cookie("token",makeToken(request,0))
                    return response
                except Exception as inst:
                    #print inst
                    #pass
                    return HttpResponse( str(inst))

            if 'msg' in request.POST:
                try:
                    if controltoken(request) != 1:

                        response =  HttpResponse(json.dumps({'response':'err',"page":"post","token":makeToken(request)}))
                        response.set_cookie("token",makeToken(request,0))
                        #printresponse
                        return response


                    #html = getLive(0,0,None)
                    #cache.delete("live_html_0")
                    #cache.set("live_html_0",html,3600)
                    post = request.POST['msg']
                    try:
                        s = Status()
                        s.from_user = u
                        dd = datetime.datetime.now()
                        s.send_time =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                        s.last_update =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                        s.text = smart_unicode(request.POST['msg'], encoding='utf-8', strings_only=False, errors='strict')
                        #return HttpResponse(int(request.POST['usemood']))
                        if int(request.POST['usemood']) > 0:
				s.mood_use = 1
			else:
				s.mood_use = 0
			s.mood_point = float(request.POST['mood'])
                        s.save()
                        k = userActions()
                        k.from_user = u
                        k.post = s
                        k.times = md()
                        k.save()
                        ##printu[0]
                    except Exception as e:
                        return HttpResponse(str( e))
                        pass
                    response = HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                    response.set_cookie("token",makeToken(request,0))
                    return response
                except Exception as e:
                    #printe
                    pass
            if 'comment' in request.POST:
                try:
                    post = request.POST['comment']
                    c= Comments.objects.filter(from_user = u , id=post)
                    if c.count() > 0:
                        c.delete()
                        return HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                    else:
                        return HttpResponse("err")
                except:
                    pass
            if 'like' in request.POST:
                try:
                    post = request.POST['like'].replace("p_","")
                    s = Status.objects.filter(id=post).get()

                    s.last_update = md()
                    s.save()
                    s.saveLike(u,md())
                    u.user_likes = u.user_likes + 1
                    u.save()
                    return HttpResponse("ok")

                except Exception as e:
                    #printe
                    return HttpResponse("err")
            if 'unlike' in request.POST:
                try:
                    post = request.POST['unlike'].replace("p_","")
                    s = Status.objects.filter(id=post).get()
                    s.deleteLike(u)
                    u.user_likes = u.user_likes - 1
                    u.save()
                    return HttpResponse("ok")

                except Exception as e:
                    print e
                    return HttpResponse("err")

        
        u = UserProfiles.objects.filter(user=request.user).get()

 
        return MakingRender("main.html",request,{'user':u})


#@login_required(login_url='/login')
def messages(request):
    return MakingRender("messages.html",request)

#@login_required(login_url='/login')
def myprofile(request):
    return MakingRender("messages.html",request)

#@login_required(login_url='/login')
def changepass(request):
    return MakingRender("messages.html",request)


#@login_required(login_url='/login')
def updatepic(request):
    return MakingRender("messages.html",request)

from django.contrib.auth import logout

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

def register(request):
    
    return MakingRender("register.html",request)


        
