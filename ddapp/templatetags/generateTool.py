'''
Created on 10.Kas.2010

@author: Administrator
'''
from django.template import Library
from django.conf import settings
from django.template import Context, loader
from duygudrm.ddapp.models import fallowers
from duygudrm.ddapp.extras.ip import controlIPL
from django import template

import time
import memcache

register = Library()
import json
cache = memcache.Client(['127.0.0.1:11211'])


class getfallow(template.Node):
    def __init__(self, format_string):
        self.format_string =  template.Variable(format_string)
    def render(self, context):
         #print context
         request = context['request']
         try:
             if self.format_string.resolve(context) != None:
                 uu = self.format_string.resolve(context)
                 if request.user.is_authenticated() and str(uu) != str(request.user):
                     a = fallowers.objects.filter(from_user=request.user,to_user=uu).count()
                     if a == 1:
                         return "<a href='#' class='unfallow' rel='"+str(uu)+"'><span>Unfallow</span></a>"
                     else:
                         return "<a href='#' class='fallow' rel='"+str(uu)+"'><span>Fallow</span></a>"
                 else:
                    return ""
         except Exception as e:
             print e
             pass
         return ""

@register.tag
def do_fallow(parser,token):
    try:
    # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except:
        pass

    return getfallow(format_string)
register.tag('fallow', do_fallow)



class getelm(template.Node):
    
    def render(self, context):
         #print context
         request = context['request']
         ip = request.META['REMOTE_ADDR']
         return controlIPL(ip)

        
@register.tag
def do_country(parser,token):
    try:
    # split_contents() knows not to split quoted strings.
        tag_name, format_string = token.split_contents()
    except:
        pass

    return getelm()
register.tag('country', do_country)







@register.filter
def generatepost(post,user):
    try:
        if user.user_id != "":
            ulogin = 1
        else:
            ulogin = 0
    except:
        ulogin = 0

    import hashlib
    m = hashlib.md5()
    c =Context({'posts': post,"user":user,"userlogin":ulogin})
    m.update(str(c))
    zr = m.hexdigest()

    render = cache.get("%s_%s" % (zr,ulogin))

    if render != None:
        return render


    t = loader.get_template("post_template.html")
   
    
    render = t.render(c)
    cache.set("%s_%s" % (zr,ulogin),render,360000)
    return render

@register.filter
def coord(post):

    x,y = post.split(",")

    return "left:"+x+"px;top:"+y+"px";


@register.filter
def generateurl(u,rewrite):

    try:
        import hashlib
        m = hashlib.md5()
        m.update("short_%s_%s" % (u,rewrite))
        zr = m.hexdigest()
        token = cache.get(zr)
        if token != None:
            return token
            
        from duygudrm.ddapp.models import shorturi
        k = shorturi.objects.filter(user=str(u),post=rewrite)
        if k.count() == 0:
            s = shorturi()
            s.user = str(u)
            s.post = rewrite
            s.save()
            from duygudrm.ddapp.extras import shorter
            surl = shorter.encode_url(s.id)
           
            s.short = surl
            s.save()
           
           
            return surl
        else:
            z = k.get()
            cache.set(zr,z.short,864000)
            return z.short
    except:
        pass




@register.filter
def comments(val):
    
    data = json.loads(val)
    return data
register.filter('comments', comments)



@register.filter
def commentsc(val):

    data = json.loads(val)
    return len(data)
register.filter('comments', comments)
@register.filter
def commentst(val):
    all = list()
    data = json.loads(val)
    
    data[0]['t'] = 1
    
    data[1]['t'] = 2
    data[len(data)-1]['t'] = 3
    data[len(data)-1]['count'] = len(data)-3
    all.append(data[0])
    all.append(data[1])
    all.append( data[len(data)-1])
    return all
register.filter('commentst', commentst)

def commentsx(val):
    all = list()
    data = json.loads(val)

    for i in range(2,len(data)-1):
        all.append(data[i])
    return all
register.filter('commentsx', commentsx)

@register.filter
def strto(val):
    return str(val)
register.filter('strto', strto)


@register.filter
def likech(val,user):
    data = json.loads(val)
    lets_me = 0
    if data != None:
        if user != None:
            for i in data:
                #print i
                if i['username'] == str(user.user):
                    lets_me = 1
    if lets_me == 1:
        return "plike_on"
    else:
        return "plike";
register.filter('likech', likech)


@register.filter
def likes(val,user):
    
    data = json.loads(val)
    lets_me = 0
    if data != None:
        if user != None:
            for i in data:

                if i['username'] == str(user.user):
                    lets_me = 1
        text = ""
        if lets_me == 1 and len(data) == 1:
            text = text + "<a href='/' class='upro first'>Bunu Begendin</a>"
        else:
            if len(data) > 3 and lets_me == 0:
                text = text +"<a class='upro first' href='/"+data[1]['rewrite']+"' >"+data[1]['username']+"</a>,<a href='/"+data[1]['rewrite']+"' class='upro'>"+data[1]['username']+"</a> ve <a href='#' rel='"+val+"'>" + str(len(data)-2) + " kisi</a> daha begendi."
            elif len(data) > 3 and lets_me == 1:
                text = text +"<a href='/"+str(user.rewrite)+"' class='upro first'>Sen</a> , <a href='/"+data[1]['rewrite']+"' class='upro'>"+data[1]['username']+"</a>  ve  <a href='#' rel='"+val+"'>" + str(len(data)-2) + " kisi</a> daha begendi."
            elif len(data) < 3:
                text = ""
                f = 0
                for i in data:
                    if text != "":
                        text = text + ","

                    if f==0:
                        f=1
                        text =text +  "<a class='upro first' href='/"+i['rewrite']+"' >"+i['username']+"</a>"
                    else:
                        text =text +  "<a class='upro' href='/"+i['rewrite']+"' >"+i['username']+"</a>"
                if text != "":
                    text = text +" bunu begendi."
        return text;
    
    return len(data)
register.filter('likes', likes)

    
    
