# -*- coding: utf-8 -*-
'''
Created on 04.Kas.2010

@author: Administrator
'''
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
import json , os
import time , StringIO , Image
import memcache
from duygudrm.ddapp.models import UserProfiles

cache = memcache.Client(['192.168.1.3:11211'])


def MakingRender(template,request=None,params={}):
    
    c = params
    c.update(csrf(request))
    c['time'] = md()
    
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
    image.save(output_filename, image.format) 
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


def handle_uploaded_file(f,id):
    print f.name
    destination = open('statics/images/users/'+id+"_"+f.name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    #i = open('statics/images/users/'+id+"_"+f.name, 'r')
    #imagefile  = StringIO.StringIO(i.read())
    thumbnail('statics/images/users/'+id+"_"+f.name)

    
    return 'statics/images/users/'+id+"_"+f.name

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
    


def user(request,x):
    if not request.user.is_authenticated():
        return MakingRender("index.html",request)
    else:
        u2 = UserProfiles.objects.filter(user=request.user).get()
        try:
            file = handle_uploaded_file(request.FILES['file'],u2.id)
            u2.avatar = file
            u2.save()
            return HttpResponse("ok")
        except Exception as inst:
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
@csrf_protect 
def index(request):
    if not request.user.is_authenticated():
        return MakingRender("index.html",request)
    else:
        
        if len(request.POST) > 0:
            u = UserProfiles.objects.filter(user=request.user).get()
            try:
                t = request.POST['t']
                print md(),t
                
                all = []
                try:
                    all = getLastest(t,u)
                except:
                    pass
                #if len(all) == 0:
                #    all = None
                print all
                k = {'time':md(),"result":all}
                print json.dumps(k)
                return HttpResponse(json.dumps(k))
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
                
                
                return HttpResponse("ok")
            except Exception as inst:
                pass
                #return HttpResponse( str(inst))
            try:
                
                html = getLive(0,0,None)
                cache.delete("live_html_0")
                cache.set("live_html_0",html,3600)
                post = request.POST['msg']
                s = Status()
                s.from_user = u
                dd = datetime.now()
                s.send_time =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                s.last_update =  time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
                s.text = request.POST['msg']
                s.mood_point = float(request.POST['mood'])
                s.save()
                k = userActions()
                k.from_user = u
                k.post = s
                k.times = md()
                k.save()
                return HttpResponse("ok")
            except:
                pass
            
            try:
                post = request.POST['comment']
                c= Comments.objects.filter(from_user = u , id=post)
                if c.count() > 0:
                    c.delete()
                    return HttpResponse("ok")
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

        