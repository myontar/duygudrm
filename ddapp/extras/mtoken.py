# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="John"
__date__ ="$28.Kas.2010 02:10:48$"

import memcache


from datetime import datetime
import time
cache = memcache.Client(['192.168.1.4:11211'])
def md():
    dd = datetime.now()
    return time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
def controltoken(request):
    token = cache.get("token_%s" % str(request.user.id))
    print "check token"
    print token
    if token == None:
        return 0
    else:
        if "token" in request.GET:
            if token == request.GET['token']:
                return 1
            else:
                return 0
        if "token" in request.POST:
            print "gelen"
            print request.POST['token']
            if token == request.POST['token']:
                return 1
            else:
                return 0
    return 0
                

def makeToken(request,fake=1):
    try:
        import hashlib
        token = hashlib.sha224(str(md())+"_sikertirimUlansizi!!!"+str(request.user.id)).hexdigest()
        #request.COOKIE['token'] = token
        if fake == 0:
            print "set cookie"
            cache.set("token_%s" % str(request.user.id),token,180)
        #print cache.get("token_%s" % str(request.user.id))
        return token
    except Exception as e:
        print "cache"
        print e
        return None
