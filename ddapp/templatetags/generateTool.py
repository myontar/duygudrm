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
def likes(val,user):
    data = json.loads(val)
    lets_me = 0
    for i in data:
        if i.user == user.user:
            lets_me = 1
    return {'me':lets_me,'data':data,'count':len(data)}
register.filter('likes', likes)

    
    