#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
'''
Created on 04.Kas.2010

@author: Administrator
'''


from django.db import models
from django.db.models.signals import post_save  
from django.contrib.auth.models import User
from django.core.context_processors import csrf
from datetime import datetime
from duygudrm.ddapp.extras.mtoken import makeToken
from django.contrib.auth.backends import ModelBackend
import memcache
cache = memcache.Client(['127.0.0.1:11211'])
import time


class MyLoginBackend(ModelBackend):
    """Return User record if username + (some test) is valid.
       Return None if no match.
    """

    def authenticate(self, username=None, password=None, request=None, external=None):
        try:
            print "auth "
            user = User.objects.get(username=username)
            print user.username
            #user.backend = 'duygudrm.ddapp.models.MyLoginBackend'
            if external == None and user.password == None:
                print "external error"
                return None
            if user.password != None and external == None:
                print "pass error"
                if user.password != password:
                    return None
            # plus any other test of User/UserProfile, etc.
            return user # indicates success
        except User.DoesNotExist:
            print username
            print "errr"
            return None
    # authenticate
# class MyLoginBackend

def md():
    dd = datetime.now()
    return time.mktime((dd.year,dd.month,dd.day,dd.hour,dd.minute,dd.second,0,0,0))
def avatar(av):
    if av == "":
        return "/statics/images/defuser.png"
    else:
        return av


def findAll(arr,key,val):
    for i in arr:
        if i[key] == val:
            return True
    return False


def getLastPost(ahuser,user,id):
    from django.template import Context, loader




    asx = list()
    a = Status.objects.filter(id__lt=id).order_by("-last_update")[0:10].all()
    for z in a:

        try:
            ##print findAll(asx,"id",z.post.id)
            st = findAll(asx,"id",z.id)
            ##print str(st)
            kr = int(z.last_update)
            
            #print str(st)
            if st == False:
                ##print z.post.id

                print z.id
                u2 = {"id":z.id,"rewrite":z.rewrite,"mood_use":z.mood_use,"text":  z.text,"last_update": int(z.last_update),"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"mood":z.mood_point,"comments":z.comment_list,"likes":z.like_list,"time":z.send_time}
                #x.append(u2)
                #print u2
                t = loader.get_template("single_post.html")
                c = {'x': u2,"user":user,"userlogin":ahuser}

                c =Context(c)
                #print x
                html = t.render(c)
                #print html
                #token = html.split('csrfmiddlewaretoken')[1].split("value")[1].split("'")[1]

                #print html
                u = {"id":z.id,"last_update":z.last_update,"html":html}
                #print "burda"
                asx.append(u)
                #print "burda"

        except Exception as inst:
            print type(inst)
            print inst



    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    return asx

def getLive(timex,ahuser,user):
    from django.template import Context, loader
    asx = list()
    a = Status.objects.filter(last_update__gt=timex).order_by("-last_update")[0:10].all()
    

    for z in a:
        
        try:
            ##print findAll(asx,"id",z.post.id)
            st = findAll(asx,"id",z.id)
            ##print str(st)
            kr = int(z.last_update)
            sss = int(timex)
            if kr > sss:
                #print str(st)
                if st == False:
                    ##print z.post.id
                    print "###############################################"
                    print ahuser
                    u2 = {"id":z.id,"rewrite":z.rewrite,"mood_use":z.mood_use,"text":  z.text,"last_update": int(z.last_update),"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"mood":z.mood_point,"comments":z.comment_list,"likes":z.like_list,"time":z.send_time,"userlogin":ahuser}
                    #x.append(u2)
                    #print u2
                    #print u2
                    t = loader.get_template("single_post.html")
                    c = {'x': u2,"user":user}

                    c =Context(c)
                    #print x
                    html = t.render(c)
                    #print html
                    #token = html.split('csrfmiddlewaretoken')[1].split("value")[1].split("'")[1]

                    #print html
                    u = {"id":z.id,"last_update":z.last_update,"html":html}
                    #print "burda"
                    asx.append(u)
                    #print "burda"                
                   
        except Exception as inst:
            print type(inst)
            print inst   
        
        
        
    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    return asx

def getLastest(timex,user,request):
    from django.template import Context, loader

    

    a = Status.objects.raw("""SELECT
u.* , u2.* , s.*
FROM
ddapp_status as s INNER JOIN
ddapp_userprofiles as u2 on u2.id = s.from_user_id
LEFT JOIN auth_user as u on u.id = u2.user_id ,
ddapp_useractions as a
WHERE
((s.id = a.post_id and a.from_user_id = %s) or (a.post_id = s.id and s.from_user_id = %s)) and s.last_update > %s   group by s.id ORDER BY s.last_update desc

""", [user.id,user.id,timex])

    ulogin = 1
    #,post=hidePost.objects.filter(from_user=self.user).all()
    asx = list()
    for z in a:
        
        try:
            #try:
                ##print findAll(asx,"id",z.post.id)
            
            ##print str(st)
            
                #print str(st)
               
                    ##print z.post.id
                    #x = []
                    #print z.username
                    u2 = {"id":z.id,"rewrite":z.rewrite,"mood_use":z.mood_use,"text":  z.text,"last_update": int(z.last_update),"from_user":z.username,"user":z.username,"attachments":z.attachments,"mood":z.mood_point,"comments":z.comment_list,"likes":z.like_list,"time":z.send_time,"userlogin":ulogin}
                    #x.append(u2)
                    t = loader.get_template("single_post.html")
                    c = {'x': u2,"user":user,"userlogin":ulogin}

                    c =Context(c)
                    #print x
                    html = t.render(c)
                    #token = html.split('csrfmiddlewaretoken')[1].split("value")[1].split("'")[1]

                    #print html
                    u = {"id":z.id,"last_update":z.last_update,"html":html}
                    #print "burda"
                    asx.append(u)
                        #print asx
            #except Exception as inst:
            #    print type(inst)
            #    print inst
    
        except Exception as e:
            print e
            #print "err"
    
    r = csrf(request)
    token = makeToken(request)
    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    
    return [asx,token]
import re
def htc(m):
    return chr(int(m.group(1),16))
def urldecode(url):
    rex=re.compile('%([0-9a-hA-H][0-9a-hA-H])',re.M)
    return rex.sub(htc,url) 
def msearch(query,user,request):
    from django.template import Context, loader

    print urldecode(query)
    a = Status.objects.filter(text__contains=urldecode(query)).all()

    ulogin = 1
    #,post=hidePost.objects.filter(from_user=self.user).all()
    asx = list()
    for z in a:
        print z
        try:
            #try:
                ##print findAll(asx,"id",z.post.id)

            ##print str(st)

                #print str(st)

                    ##print z.post.id
                    #x = []
                    #print z.username
                    u2 = {"id":z.id,"rewrite":z.rewrite,"mood_use":z.mood_use,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
                    #x.append(u2)
                    print u2
                    t = loader.get_template("single_post.html")
                    c = {'x': u2,"user":user,"userlogin":ulogin}

                    c =Context(c)
                    #print x
                    html = t.render(c)
                    #token = html.split('csrfmiddlewaretoken')[1].split("value")[1].split("'")[1]

                    #print html
                    u = {"id":z.id,"last_update":z.last_update,"html":html}
                    print u
                    #print "burda"
                    asx.append(u)
                        #print asx
            #except Exception as inst:
            #    print type(inst)
            #    print inst

        except Exception as e:
            print e
            #print "err"
    a = Status.objects.filter(comment_list__contains=urldecode(query)).all()

    ulogin = 1
    #,post=hidePost.objects.filter(from_user=self.user).all()
    
    for z in a:
        print z
        try:
            #try:
                ##print findAll(asx,"id",z.post.id)

            ##print str(st)

                #print str(st)

                    ##print z.post.id
                    #x = []
                    #print z.username
                    u2 = {"id":z.id,"rewrite":z.rewrite,"mood_use":z.mood_use,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
                    #x.append(u2)
                    print u2
                    t = loader.get_template("single_post.html")
                    c = {'x': u2,"user":user,"userlogin":ulogin}

                    c =Context(c)
                    #print x
                    html = t.render(c)
                    #token = html.split('csrfmiddlewaretoken')[1].split("value")[1].split("'")[1]

                    #print html
                    u = {"id":z.id,"last_update":z.last_update,"html":html}
                    print u
                    #print "burda"
                    asx.append(u)
                        #print asx
            #except Exception as inst:
            #    print type(inst)
            #    print inst

        except Exception as e:
            print e
            #print "err"

    r = csrf(request)
    token = makeToken(request)
    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    return [asx,token]



def list_comments(query,request):
    from django.template import Context, loader


    asx = list()

    a = Status.objects.filter(comment_list__contains='"'+query+'"').order_by("-last_update")
   
    print a.query
    a = a.all()
    ulogin = 1
    #,post=hidePost.objects.filter(from_user=self.user).all()

    for z in a:
        print z
        try:
            #try:
                ##print findAll(asx,"id",z.post.id)

            ##print str(st)

                #print str(st)

                    ##print z.post.id
                    #x = []
                    #print z.username
                    u = {"id":z.id,"rewrite":z.rewrite,"mood_use":z.mood_use,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
                    #x.append(u2)
                   
                    #print "burda"
                    asx.append(u)
                        #print asx
            #except Exception as inst:
            #    print type(inst)
            #    print inst

        except Exception as e:
            print e
            #print "err"

    r = csrf(request)
    token = makeToken(request)
    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    return asx

def list_likes(query,request):
    from django.template import Context, loader


    asx = list()

    a = Status.objects.filter(like_list__contains='"'+query+'"').order_by("-last_update")

    print a.query
    a = a.all()
    ulogin = 1
    #,post=hidePost.objects.filter(from_user=self.user).all()

    for z in a:
        print z
        try:
            #try:
                ##print findAll(asx,"id",z.post.id)

            ##print str(st)

                #print str(st)

                    ##print z.post.id
                    #x = []
                    #print z.username
                    u = {"id":z.id,"mood_use":z.mood_use,"rewrite":z.rewrite,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
                    #x.append(u2)

                    #print "burda"
                    asx.append(u)
                        #print asx
            #except Exception as inst:
            #    print type(inst)
            #    print inst

        except Exception as e:
            print e
            #print "err"

    r = csrf(request)
    token = makeToken(request)
    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    return asx



class tags(models.Model):
    tag     = models.CharField(max_length=40,default='',null=True)
    user            = models.ForeignKey(User)


class UserProfiles(models.Model):
    user            = models.ForeignKey(User)
    rewrite         = models.SlugField(null=True)
    #user_last_entry =
    britdate        = models.IntegerField(default=0,null=True)
    britdate_show   = models.CharField(max_length=15,default='',null=True)
    avatar          = models.CharField(max_length=255,default='',null=True)
    webpage         = models.CharField(max_length = 200,default='',null=True)
    last_visit      = models.IntegerField(null=True,default=0)
    city            = models.CharField(max_length = 200,default='',null=True)
    gender          = models.SmallIntegerField(null=True,default=0)
    bio             = models.CharField(max_length=255,default='',null=True)
    user_fallow     = models.IntegerField(default=0,null=True)
    user_fallower   = models.IntegerField(default=0,null=True)
    user_comments   = models.IntegerField(default=0,null=True)
    user_likes      = models.IntegerField(default=0,null=True)
    user_msg_alert  = models.SmallIntegerField(null=True,default=0)
    user_add_alert  = models.SmallIntegerField(null=True,default=0)
    user_not_alert  = models.SmallIntegerField(null=True,default=0)
    def __unicode__(self):
        return str(self.user)
    def fallowers(self):
        a = fallowers.objects.filter(from_user = self).all()
        return a
    def fallwoersCount(self):


        from django.db.models import Avg , Max , Min ,Count
        a = fallowers.objects.filter(from_user = self).annotate(countall=Count('id'))
        return int(a['countall'])
        
       

    def allcount(self):
        #z = Status.objects.filter(from_user = self).count()

        #print z
        return 0

    def moodcount(self):
        print "##################################################"
        #z = Status.objects.filter(mood_use = 1 , from_user = self).count()
        
        #print z
        return 0

    def fallowed(self):
        from django.db.models import Avg , Max , Min ,Count
        a = fallowers.objects.filter(to_user = self).all()
        return a
    
    def fallowedCount(self):
        from django.db.models import Avg , Max , Min ,Count
        a = fallowers.objects.filter(to_user = self).annotate(countall=Count('id'))
        return int(a['countall'])
    
    def getStat(self):
        from django.db.models import Avg , Max , Min ,Count
        try:
            r = Status.objects.raw(""" SELECT `ddapp_status`.`id`, `ddapp_status`.`from_user_id`, `ddapp_status`.`send_time`, `ddapp_status`.`text`, `ddapp_status`.`attachments`, `ddapp_status`.`mood_point`, `ddapp_status`.`mood_use`, `ddapp_status`.`last_update`, `ddapp_status`.`like_list`, `ddapp_status`.`rewrite`, `ddapp_status`.`comment_list`, MIN(`ddapp_status`.`mood_point`) AS `mood_point__min`, MAX(`ddapp_status`.`mood_point`) AS `mood_point__max`, AVG(`ddapp_status`.`mood_point`) AS `mood_point__avg` , COUNT(`ddapp_status`.`mood_point`) AS `mood_point__count`  FROM `ddapp_status` WHERE (`ddapp_status`.`mood_use` = 1  AND `ddapp_status`.`from_user_id` = %d ) GROUP BY `ddapp_status`.`from_user_id` ORDER BY NULL  """ % self.user_id)
            
        except Exception as e:
            return str(e)


        try:
            alsl = r[0]
        
            return {"ort":str(alsl.mood_point__avg)[:3],"big":str(alsl.mood_point__max),"min":str(alsl.mood_point__min),"total":alsl.mood_point__count}
        except:
            return {"ort":0,"big":0,"min":0,"total":0}
           
        return r[0]
        
    def getSelf(self):
        asx = []
        a = Status.objects.filter(from_user=self).order_by("-last_update")[0:50].all()
        for z in a:
            
            try:
                ##print findAll(asx,"id",z.post.id)
                st = findAll(asx,"id",z.id)
                ##print str(st)
                kr = int(z.last_update)
                
                
                #print str(st)
                if st == False:
                    u = {"id":z.id,"mood_use":z.mood_use,"rewrite":z.rewrite,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
            ##print z.post
            #u.update('user',z.from_user})
            # u.user = z.from_user
            
                    asx.append(u)
            except Exception as inst:
                print type(inst)
                print inst
        #asx.sort( key="last_update" )
        asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
         
        return asx

    def gen_tags(self):
        
        from django.db.models import Count
        #q = Player.objects.values('playertype').annotate(Count('games'))
        tagsl = tags.objects.filter(user=self.user).values('tag').annotate(Count('tag'))

        text = ""
        try:
            total = 0
            for i in tagsl:
                total = total + i['tag__count']
                text += '<a href="/search?q=!%s" class="cloud_mood" style="font-size:%d ;">%s</a> ' % (i['tag'],int(i['tag__count']),i['tag'])

            p = float(total) / 100.0;
            rr = 75.0 / 100.0;
            import re
            text = re.sub(r'font-size:([^\s]*)', r"font-size:' + str(int(float(float(\1) / float(p))*rr)) + 'px", text)
            text = eval("'"+text+"'")
        except Exception as e:
            return e
        return text


    def getSelfMoods(self):
        asx = []
        a = Status.objects.filter(from_user=self,mood_use=1).order_by("-last_update")[0:50].all()
        for z in a:

            try:
                ##print findAll(asx,"id",z.post.id)
                st = findAll(asx,"id",z.id)
                ##print str(st)
                kr = int(z.last_update)


                #print str(st)
                if st == False:
                    u = {"id":z.id,"mood_use":z.mood_use,"rewrite":z.rewrite,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.like_list,"comments":z.comment_list}
            ##print z.post
            #u.update('user',z.from_user})
            # u.user = z.from_user

                    asx.append(u)
            except Exception as inst:
                print type(inst)
                print inst
        #asx.sort( key="last_update" )
        asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)

        return asx

    def myStatusList(self):
        s = []
        s.append(self)
        for k in self.fallowers():
            s.append(k.to_user)
        ##print s
        
        a = userActions.objects.filter(from_user__in=s).order_by("-times")[0:50].all()
        #,post=hidePost.objects.filter(from_user=self.user).all()
        asx =  cache.get("getLastest_%s" % str(self.user.id))
        #return asx
        if asx != None:
            return asx
        asx = list()
        for z in a:
            
            try:
                ##print findAll(asx,"id",z.post.id)
                st = findAll(asx,"id",z.post.id)
                #print str(st)
                if st == False:
                    u = {"id":z.post.id,"mood_use":z.post.mood_use,"rewrite":z.post.rewrite,"text":  z.post.text,"time":z.post.send_time,"last_update":z.post.last_update,"from_user":z.post.from_user,"user":z.from_user,"attachments":z.post.attachments,"send_time":z.post.send_time,"mood":z.post.mood_point,"likes":z.post.like_list,"comments":z.post.comment_list}
                ##print z.post
                #u.update('user',z.from_user})
                # u.user = z.from_user
                
                    asx.append(u)
            except Exception as inst:
                print "burda"
                print type(inst)
                print inst
                #print userActions.objects.filter(from_user__in=s).group_by("post_id").order_by("-times").query
        #asx.sort( key="last_update" )
        #asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
        cache.set("getLastest_%s" % str(self.user.id),asx,365000)
        return asx



class UserAlerts(models.Model):
     user            = models.ForeignKey(User)
     type            = models.SmallIntegerField()
     post_id         = models.IntegerField(default=0)
     read            = models.SmallIntegerField(default=0,)


def sendAlert(user,type,post_id):
    a = User.objects.filter(username = user).get()
    s = UserAlerts()
    s.user = a
    s.type = type
    s.post_id = post_id
    s.save()
    return


class userLoginService(models.Model):
    user            = models.ForeignKey(UserProfiles)
    service         = models.CharField(max_length=200)
    service_param   = models.CharField(max_length=2000)
    service_uid     = models.CharField(max_length=200)

class UserMessages(models.Model):
    from_user   = models.ForeignKey(UserProfiles)
    to_user     = models.ForeignKey(User,related_name="to")
    is_read     = models.SmallIntegerField(default=0)
    msg_title   = models.CharField(max_length = 255)
    msg_body    = models.TextField()
    parent      = models.IntegerField(default=0)
    def __unicode__(self):
        return "%s to %s" % ( self.from_user , self.to_user)
    def getMsg(self):
        a = UserMessages.objects.filter(parent = UserMessages).get()
        return a
    def newmessage(self,froms,to,body,title):
        a           = UserMessages()
        a.from_user = froms
        a.to_user   = to
        a.msg_title = title
        a.msg_body  = body
        a.put()
    def replymsg(self,msg,body):
        a           = UserMessages()
        a.parent    = msg
        a.body      = body
        a.put()
class fallowers(models.Model):
    from_user   = models.ForeignKey(UserProfiles)
    to_user     = models.ForeignKey(UserProfiles,related_name="toa")
    def __unicode__(self):
        return str(self.from_user.user) + " -> " + str(self.to_user.user) 
    def GetStatus(self):
        a = Status.objects.filter(from_user =self.to_user).order_by("last_update").all()
        return a

class perms(models.Model):
    user            = models.ForeignKey(UserProfiles)
    feed            = models.SmallIntegerField(default=1)
    postit          = models.SmallIntegerField(default=1)
    freq            = models.SmallIntegerField(default=1)
    freq            = models.SmallIntegerField(default=1)
    dm              = models.SmallIntegerField(default=1)
    flw             = models.SmallIntegerField(default=1)
    

class postit(models.Model):
    user            = models.ForeignKey(UserProfiles)
    to_user         = models.ForeignKey(UserProfiles,related_name="tototo")
    text            = models.CharField(max_length=100)
    coord           = models.CharField(max_length=100)
    onay            = models.SmallIntegerField(default=0)



class shorturi(models.Model):
    short           = models.CharField(max_length=100)
    user            = models.CharField(max_length=200)
    post            = models.CharField(max_length=200)
class Status(models.Model):
    from_user       = models.ForeignKey(UserProfiles)
    send_time       = models.IntegerField()
    text            = models.TextField()
    attachments     = models.CharField(max_length=1000)
    mood_point      = models.FloatField()
    mood_use	    = models.SmallIntegerField(null=True,default=0)
    last_update     = models.IntegerField()
    like_list       = models.TextField(null=True,default="[]")
    rewrite         = models.CharField(null=True,default="piii",max_length=1000)
    comment_list    = models.TextField(null=True,default="[]")

    def save(self):
        cache.delete("getLastest_%s" % self.from_user.user.id)

        try:
            if len(self.text) > 100:
                rewrite = self.text[:100]
            else:
                rewrite = self.text
            import re

            import sys
            rewrite = u"%s" % rewrite
            re_strip = re.compile(r'[^\w\s-]')

            #text =  text.decode("utf-8")

            tmp = rewrite.lower().replace("ı","i").replace("ç","c").replace("ş","s").replace("ö","o").replace("ü","u").replace("ğ","g")
            #tmp = text.lower()

            re_dashify = re.compile(r'[-\s]+')
            cleanup= re_strip.sub('', tmp).strip().lower()
            rewrite =  re_dashify.sub('-', cleanup)
            k = True
           
            while k:
                s = Status.objects.filter(rewrite=rewrite , from_user=self.from_user).count()
                if s > 0:
                    rewrite = rewrite +"-1"
                else:
                    k = False
            self.rewrite = rewrite.lower()
        except Exception as e:
            print e
        try:
            super(Status, self).save() # Call the "real" save() method
            id = self.id
            import re
            try:
                REGEX_Ment          = "((![^\s]*))"
                regex = re.compile(REGEX_Ment)
                ment = regex.findall(self.text)
                for i in ment:
                    print i
                    t = tags()
                    t.tag = str(i[0]).replace("!","")
                    t.user = self.from_user.user
                    t.save()




            except Exception as e:
                print e


            
            REGEX_Ment          = "((@[^\s]*))"
            regex = re.compile(REGEX_Ment)
            ment = regex.findall(self.text)
            for i in ment:
                sendAlert(i[0].replace("@",""),1,id)


        except Exception as e:
            print e


    def saveComment(self,user,text,time):
        import json
        data = json.loads(self.comment_list)
        id = len(data)+13
        

        
        
        #sendAlert(self.id,self.from_user.user,2)


        try:
            if str(self.from_user.user) != str(user.user):
                sendAlert(str(self.from_user.user),2,self.id)
        except:
            pass
        try:
            for i in data:
                if i['username'] != str(self.from_user.user) and i['username'] != str(user.user):
                    sendAlert(str(i['username']),2,self.id)
        except:
            pass
        
        data.append({"id":id,"username":str(user.user),"rewrite":user.rewrite,"text":text,"date":time})
        

        self.comment_list = json.dumps(data)
        self.save()
        k2 = userActions()
        k2.from_user = user
        k2.post = self
        k2.times = time
        k2.post_id = self.id
        k2.save()
        
    def saveLike(self,user,time):
        import json
        data = json.loads(self.like_list)
        data.append({'username':str(user.user),"rewrite":user.rewrite})
        self.like_list = json.dumps(data)
        self.save()
        k2 = userActions()
        k2.from_user = user
        k2.post = self
        k2.times = time
        k2.post_id = self.id
        k2.save()

    def deleteLike(self,user):
        import json
        data = json.loads(self.like_list)
        tmp_data = []
        save = 0
        for i in data:
            if i['username'] != str(user.user):
                tmp_data.append(i)
            else:
                save = 1
        if save == 1:
            self.like_list = json.dumps(tmp_data)
            self.save()
    
    def editComment(self,id,user,text):
        import json
        cache.delete("getLastest_%s" % self.from_user.user.id)
        data = json.loads(self.comment_list)
        tmp_data = []
        save = 0
        for i in data:
            if int(id) != int(i['id']):
                tmp_data.append(i)
            else:
                if i['username'] != str(user.user):
                    tmp_data.append(i)
                else:
                    i['text'] = text
                    tmp_data.append(i)
                    save = 1
        if save == 1:
            self.comment_list = json.dumps(tmp_data)
            self.save()
      
    def deleteComment(self,id,user):
        import json
        cache.delete("getLastest_%s" % self.from_user.user.id)
        data = json.loads(self.comment_list)
        tmp_data = []
        save = 0
        for i in data:
            if int(id) != int(i['id']):
                tmp_data.append(i)
            else:
                if i['username'] != str(user.user):
                    tmp_data.append(i)
                else:
                    save = 1
        if save == 1:
            self.comment_list = json.dumps(tmp_data)
            self.save()
        
          
    def likes(self):
        r = Likes.objects.filter(from_status = self)
        if r.count() > 0:
            return {"likes":r.all()[0],"count":(int(r.count())-1)}
        
    def getComments(self):
        r = Comments.objects.filter(from_status=self.from_user).get()
        return r
    def getCommentsCount(self):
        r = Comments.objects.filter(from_status=self)
        #return r
        if r.count() < 3:
            return {"count":int(r.count()),"first":r.all(),"last":None}
        else:
            z = (int(r.count())-1)
            return {"count2":z-2,"count":z,"first":r.all()[:2],"last":r.all()[z:z+1]}


class Comments(models.Model):
    from_status = models.ForeignKey(Status)
    from_user   = models.ForeignKey(UserProfiles)
    text        = models.CharField(max_length=1000)
    ctime       = models.IntegerField(null=True,default=1289068211)
    #likes       = models.IntegerField()

class Likes(models.Model):
    from_status = models.ForeignKey(Status)
    from_user   = models.ForeignKey(UserProfiles)
    


class CLikes(models.Model):
    from_comments = models.ForeignKey(Comments)
    from_user   = models.ForeignKey(UserProfiles)
    
class hidePost(models.Model):
    from_user   = models.ForeignKey(UserProfiles)
    post        = models.ForeignKey(Status)
    
class userActions(models.Model):
    from_user   = models.ForeignKey(UserProfiles)
    post        = models.ForeignKey(Status)
    times       = models.IntegerField(null=True,default=1289068211)
    action_type = models.IntegerField(null=True,default=0)
    posts_id     = models.CharField(null=True,default="",max_length=255)
class myAlerts(models.Model):
    from_user   = models.ForeignKey(UserProfiles)
    post        = models.IntegerField()
    typ         = models.SmallIntegerField()

    
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfiles.objects.get_or_create(user=instance)  






post_save.connect(create_user_profile, sender=User) 
