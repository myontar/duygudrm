'''
Created on 10.Kas.2010

@author: Administrator
'''
from django.template import Library
from django.conf import settings
from django.template import Context, loader

import time


register = Library()
import json


@register.filter
def generatepost(post,user):
    print post
    t = loader.get_template("post_template.html")
    c =Context({'posts': post,"user":user})

    return t.render(c)


@register.filter
def generateurl(u,rewrite):

    from duygudrm.ddapp.models import shorturi
    k = shorturi.objects.filter(user=str(u),post=rewrite)
    if k.count() == 0:
        s = shorturi()
        s.user = str(u)
        s.post = rewrite
        s.save()
        from duygudrm.ddapp.extras import shorter
        surl = shorter.encode_url(s.id)
        print "sid"
        print s.id
        s.short = surl
        s.save()
        print surl
        print "sid2"
        print s.id
        return surl
    else:
        z = k.get()
        print "shorter"
        print z.short
        return z.short




@register.filter
def comments(val):
    
    data = json.loads(val)
    return data
register.filter('comments', comments)

@register.filter
def strto(val):
    return str(val)
register.filter('strto', strto)


@register.filter
def likech(val,user):
    data = json.loads(val)
    lets_me = 0
    if data != None:
        for i in data:
            print i
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
        for i in data:
            print i
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
        return text;
    
    return len(data)
register.filter('likes', likes)

    
    