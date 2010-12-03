# -*- coding: utf-8 -*-
'''
Created on 04.Kas.2010

@author: Administrator
'''
import os.path
from django.utils.encoding import *
from duygudrm.ddapp.extras.mtoken import makeToken , controltoken
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
from datetime import datetime
from django.contrib.auth.decorators import login_required
import json , os ,sys
import time , StringIO , Image
import memcache

from duygudrm.ddapp.models import UserProfiles

cache = memcache.Client(['192.168.1.3:11211'])


def MakingRender(template,request=None,params={}):
    
    c = params
    c.update(csrf(request))
    c['time'] = md()
    c['ttoken'] = makeToken(request,0)
    return render_to_response(template, c)

def md():
    dd = datetime.now()
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
    image = image.resize(size, Image.ANTIALIAS)

    # get the thumbnail data in memory.
    if not output_filename:
        output_filename = filename
    image.save(output_filename, image.JPEG)
    return output_filename

def handle_uploaded_file2(f):
    print f.name
    destination = open('statics/users/'+f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    #i = open('statics/images/users/'+id+"_"+f.name, 'r')
    #imagefile  = StringIO.StringIO(i.read())
   
    
    return f.name


def handle_uploaded_file(f,username):
    print f.name
    print 'statics/users/avatar/'+username
    e = str(f.name).split(".")[len(str(f.name).split("."))-1]
    print 'statics/users/avatar/'+username+"."+e
    
    try:
        destination = open('statics/users/avatar/'+username+"."+e, 'ab+')
        for chunk in f.chunks():
            destination.write(chunk)
        destination.close()
        #i = open('statics/images/users/'+id+"_"+f.name, 'r')
        #imagefile  = StringIO.StringIO(i.read())
    except:
        print "edeee"
    print "geldik"
    thumbnail('statics/users/avatar/'+username+"."+e,(120,120),'statics/users/avatar/'+username+".jpg")

    
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
    #return HttpResponse(str(html))
    if html == None:
        
        html = getLive(0,u,u2)
        cache.set("live_html_%d" % u,html,3600)
    
    return MakingRender("live.html",request,{'user':u2,"isuser":u,"html":html})
    
def getsinglepost(request,x,y):
    z = Status.objects.filter(from_user__user__username=x,rewrite=y).get()
    asx = []
    u = {"id":z.id,"rewrite":z.rewrite,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
            ##print z.post
            #u.update('user',z.from_user})
            # u.user = z.from_user

    asx.append(u)
    print asx
    return MakingRender("profile_1.html",request,{'user':user,'post':asx})
def user(request,x):
    if not request.user.is_authenticated():
        return MakingRender("index.html",request)
    else:
        u2 = UserProfiles.objects.filter(user=request.user).get()
        try:
            print u2.id
            file = handle_uploaded_file(request.FILES['file'],u2.user.username)
            u2.avatar = file
            u2.save()
            return HttpResponse("ok")
        except Exception as inst:
                print "avatar errr"
                print type(inst)
                print inst
        uname = request.path.replace("/","")
        u = UserProfiles.objects.filter(rewrite=x).get()
        
        takip = fallowers.objects.filter(from_user=u2,to_user=u).count()
        return MakingRender("profile.html",request,{'user':u,"takip":int(takip),"me":u2})
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
        print "############################ upload ok"
    except Exception as inst:
            print type(inst)
            print  str(inst)
            
    return HttpResponse("dememe")

def proxy(request):
    import hashlib 
    h = request.GET['p']
    z = hashlib.md5()
    z.update(h)
    h = z.hexdigest()
    
    if os.path.exists("/home/django/duygudrm/statics/proxy/"+h):
        return HttpResponse(open("/home/django/duygudrm/statics/proxy/"+h,"rb").read())
    else:
        import urllib2 , urllib
        std_headers = {
                'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.11) Gecko/20101019 Firefox/3.6.11',
                'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
            }
        print request.GET['p']
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
        print request.GET['p']
        request = urllib2.Request(request.GET['p'], None, std_headers)
        video_info_webpage = urllib2.urlopen(request).read()
        f = open("/home/django/duygudrm/statics/imgproxy/"+h,"a+")
        f.write(video_info_webpage)
        f.close()
        thumbnail("/home/django/duygudrm/statics/imgproxy/"+h)
        f = open("/home/django/duygudrm/statics/imgproxy/"+h,"rb").read()
        return HttpResponse(f)



def avatarControl(request,avat):
    if os.path.exists("statics/users/avatar/"+avat):
        return redirect("statics/users/avatar/"+avat+".jpg")
    else:
        return redirect("statics/users/avatar/default.jpg")
@csrf_protect 
def index(request):
    request.encoding = 'utf-8'
    if not request.user.is_authenticated():
        return MakingRender("index.html",request)
    else:
        
        if len(request.POST) > 0:
            u = UserProfiles.objects.filter(user=request.user).get()
            try:
                if controltoken(request) != 1:
                    
                    response =  HttpResponse(json.dumps({'response':'err','oi':'poi',"token":""}))
                    response.set_cookie("token",makeToken(request,0),365)
                    print response
                    return response
                t = request.POST['t']
                print md(),t
                
                all = []
                try:
                    all = getLastest(t,u,request)
                except:
                    print "err"
                    pass
                #if len(all) == 0:
                #    all = None
                #print all
                k = {'time':md(),"result":all[0],"token":all[1]}
                print "##############################"
                print json.dumps(k)

                response =  HttpResponse(json.dumps(k))
                response.set_cookie("token",makeToken(request,0))
                return response

            except:
                pass
            
            try:
                rep = request.POST['getU']
                
                s = UserProfiles.objects.filter(rewrite__startswith=rep).all()[:20]
                r = list()
                r.append({'id':"all",'name':"Herkese"})
                for i in s:
                    r.append({'id':i.rewrite,'name':str(i.user)})
                                
                return HttpResponse(json.dumps(r))
                
            except Exception as inst:
                print type(inst)
                #return HttpResponse( str(inst))
                
            
            try:
                reply = request.POST['reply']
                s = Status.objects.filter(id=reply).get()
                s.last_update = md()
                s.save()
                s.saveComment(u,request.POST['text'],md())
                
                
                response =  HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response
            except Exception as inst:
                pass
                #return HttpResponse( str(inst))
            try:
                if controltoken(request) != 1:
                   
                    response =  HttpResponse(json.dumps({'response':'err',"page":"post","token":makeToken(request)}))
                    response.set_cookie("token",makeToken(request,0))
                    print response
                    return response
                
               
                html = getLive(0,0,None)
                cache.delete("live_html_0")
                cache.set("live_html_0",html,3600)
                post = request.POST['msg']
                try:
                    s = Status()
                    s.from_user = u
                    dd = datetime.now()
                    s.send_time =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                    s.last_update =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                    s.text = smart_unicode(request.POST['msg'], encoding='utf-8', strings_only=False, errors='strict')
                    s.mood_point = float(request.POST['mood'])
                    s.save()
                    k = userActions()
                    k.from_user = u
                    k.post = s
                    k.times = md()
                    k.save()
                    #print u[0]
                except Exception as e:
                    s = Status()
                    s.from_user = u
                    dd = datetime.now()
                    s.send_time =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                    s.last_update =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                    s.text = "buuuu"
                    s.mood_point = float(request.POST['mood'])
                    s.save()
                    k = userActions()
                    k.from_user = u
                    k.post = s
                    k.times = md()
                    k.save()
                    pass
                response = HttpResponse(json.dumps({"response:":"ok","token":makeToken(request)}))
                response.set_cookie("token",makeToken(request,0))
                return response
            except:
                print "err cached"
                pass
            
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
            
            try:
                post = request.POST['like']
                s = Status.objects.filter(id=post).get()
                
                sc = Likes.objects.filter(from_user = u,from_status=s).count()
               
                if sc == 0:
                    
                    s.last_update = md()
                    s.save()
                    k = Likes()
                    k.from_user = u
                    k.from_status = s
                    k.save()
                    k2 = userActions()
                    k2.from_user = u
                    k2.post = s
                    k2.times = md()
                    k2.save()
                    return HttpResponse("ok")
                else:
                    return HttpResponse("err")
            except:
                pass
        
        u = UserProfiles.objects.filter(user=request.user).get()
       
        return MakingRender("main.html",request,{'user':u})


@login_required(login_url='/login')
def messages(request):
    return MakingRender("messages.html",request)

@login_required(login_url='/login')
def myprofile(request):
    return MakingRender("messages.html",request)

@login_required(login_url='/login')
def changepass(request):
    return MakingRender("messages.html",request)


@login_required(login_url='/login')
def updatepic(request):
    return MakingRender("messages.html",request)


def register(request):
    
    return MakingRender("register.html",request)

def login(request):
    
    return MakingRender("login.html",request)

        