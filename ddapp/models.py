'''
Created on 04.Kas.2010

@author: Administrator
'''
# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save  
from django.contrib.auth.models import User


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

def getLive(timex,ahuser,user):
    asx = list()
    a = Status.objects.all().order_by("-last_update")[:20]
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
                    
                    html = """<span><b>%s</b>""" % z.from_user
                    if z.from_user != z.from_user:
                        html = html + ("""(<b>%s</b> araciligi ile)""" % z.from_user)
                    html = html + ("""</span> <div class="moodText">%s</div>
                                    <div>
                                        %s
                                    </div>""" % (z.mood_point,z.text))
                    
                    x = z.likes()
                    if z.likes() != None:
                        if x['count'] > -1:
                            html = html + str(x['likes'].from_user) 
                            if x['count'] > 0 :
                                html = html + " ve  "+str(x['count'])+" kisi daha begendi."
                            html= html+"<br />"
                        
                    html= html +  u"""<a href="javascript:;" class="like">Begen</a> | <a href="javascript:;" class="commentSend">Yorum Yaz</a>"""
                    if ahuser:
                        if z.from_user == user.user:
                           html = html + """ | <a href="javascript:;" class="dispost">Sil</a>           <br class="clr" />"""
                        
                    for i in z.getCommentsCount()['first']:
                        html= html + """<div class="comm" id="""+i.id+"""">"""
                        html= html + """<span>"""+str(i.from_user)+"""</span><br/>"""
                        html= html + """<div>"""+i.text+"""</div>"""
                        if ahuser:
                            if i.from_user == user.user:
                                html =  html + """<a href="javascript:;" class="discomment">sil</a>"""
                        html= html + """</div>"""
                    if z.getCommentsCount()['count'] >= 3:  
                        for i in z.getCommentsCount()['last']:
                            html= html + """<div class="comm" id="""+i.id+"""">"""
                            html= html + """<span>"""+str(i.from_user)+"""</span><br/>"""
                            html= html + """<div>"""+i.text+"""</div>"""
                            if ahuser:
                                if i.from_user == user.user:
                                    html =  html + """<a href="javascript:;" class="discomment">sil</a>"""
                            html= html + """</div>"""
                   
                        
                    
                    u = {"id":z.id,"last_update":z.last_update,"html":html}
                    #print "burda"                
                    asx.append(u)
                    #print asx
        except Exception as inst:
            print type(inst)
            print inst   
        
        
        
    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    return asx

def getLastest(timex,user):
    s = []
    s.append(user)
    #print user.user
    for k in user.fallowers():
        s.append(k.to_user)
    ##print s
    a = userActions.objects.filter(from_user__in=s).all()
    #,post=hidePost.objects.filter(from_user=self.user).all()
    asx = list()
    for z in a:
        
        try:
            ##print findAll(asx,"id",z.post.id)
            st = findAll(asx,"id",z.post.id)
            ##print str(st)
            kr = int(z.post.last_update)
            sss = int(timex)
            if kr > sss:
                #print str(st)
                if st == False:
                    ##print z.post.id
                    
                    html = """<img src="%s"><span><b>%s</b>""" % (avatar(z.post.from_user.avatar),z.post.from_user)
                    if z.from_user != z.post.from_user:
                        html = html + ("""(<b>%s</b> araciligi ile)""" % z.from_user)
                        
                    ht ="""</span> <div class="moodText">%s</div>
                                    <div>
                                        %s
                                    </div>""" % (z.post.mood_point,z.post.text)
                    html = html + ht
                    
                    x = z.post.likes()
                    if z.post.likes() != None:
                        if x['count'] > -1:
                            html = html + str(x['likes'].from_user) 
                            if x['count'] > 0 :
                                html = html + " ve  "+str(x['count'])+" kisi daha begendi."
                            html= html+"<br />"
                        
                    html= html +  u"""<a href="javascript:;" class="like">Begen</a> | <a href="javascript:;" class="commentSend">Yorum Yaz</a>"""
                    if z.post.from_user == user.user:
                       html = html + """ | <a href="javascript:;" class="dispost">Sil</a>           <br class="clr" />"""
                    
                    for i in z.post.getCommentsCount()['first']:
                        html= html + """<div class="comm" id="""+i.id+"""">"""
                        html= html + """<img src='"""+avatar(i.from_user.avatar)+"""' />"""

                        html= html + """<span>"""+str(i.from_user)+"""</span><br/>"""
                        html= html + """<div>"""+i.text+"""</div>"""
                        if i.from_user == user.user:
                            html =  html + """<a href="javascript:;" class="discomment">sil</a>"""
                        html= html + """</div>"""
                    if z.post.getCommentsCount()['count'] >= 3:  
                        html = html + """<span class="morecomment"><b>diger """+str(z.post.getCommentsCount()['count'])+""" yorumu goster</b></span>"""
                        for i in z.post.getCommentsCount()['last']:
                            html= html + """<div class="comm" id="""+i.id+"""">"""
                            html= html + """<img src='"""+avatar(i.from_user.avatar)+"""' />"""
                            html= html + """<span>"""+str(i.from_user)+"""</span><br/>"""
                            html= html + """<div>"""+i.text+"""</div>"""
                            if i.from_user == user.user:
                                html =  html + """<a href="javascript:;" class="discomment">sil</a>"""
                            html= html + """</div>"""
                        
                    
                    u = {"id":z.post.id,"last_update":z.post.last_update,"html":html}
                    #print "burda"                
                    asx.append(u)
                    #print asx
        except Exception as inst:
            print type(inst)
            print inst   
            #print "err"
            
    a = Status.objects.filter(from_user=user.user).all()
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
                    
                    html = """<span><b>%s</b>""" % z.from_user
                    if z.from_user != z.from_user:
                        html = html + ("""(<b>%s</b> araciligi ile)""" % z.from_user)
                    html = html + ("""</span> <div class="moodText">%s</div>
                                    <div>
                                        %s
                                    </div>""" % (z.mood_point,z.text))
                    
                    x = z.likes()
                    if z.likes() != None:
                        if x['count'] > -1:
                            html = html + str(x['likes'].from_user) 
                            if x['count'] > 0 :
                                html = html + " ve  "+str(x['count'])+" kisi daha begendi."
                            html= html+"<br />"
                        
                    html= html +  u"""<a href="javascript:;" class="like">Begen</a> | <a href="javascript:;" class="commentSend">Yorum Yaz</a>"""
                    if z.from_user == user.user:
                       html = html + """ | <a href="javascript:;" class="dispost">Sil</a>           <br class="clr" />"""
                    
                    for i in z.getCommentsCount()['first']:
                        html= html + """<div class="comm" id="""+i.id+"""">"""
                        html= html + """<span>"""+str(i.from_user)+"""</span><br/>"""
                        html= html + """<div>"""+i.text+"""</div>"""
                        if i.from_user == user.user:
                            html =  html + """<a href="javascript:;" class="discomment">sil</a>"""
                        html= html + """</div>"""
                    if z.getCommentsCount()['count'] >= 3:  
                        for i in z.getCommentsCount()['last']:
                            html= html + """<div class="comm" id="""+i.id+"""">"""
                            html= html + """<span>"""+str(i.from_user)+"""</span><br/>"""
                            html= html + """<div>"""+i.text+"""</div>"""
                            if i.from_user == user.user:
                                html =  html + """<a href="javascript:;" class="discomment">sil</a>"""
                            html= html + """</div>"""
                   
                        
                    
                    u = {"id":z.id,"last_update":z.last_update,"html":html}
                    #print "burda"                
                    asx.append(u)
                    #print asx
        except Exception as inst:
            print type(inst)
            print inst   
        
        
        
    #asx.sort( key="last_update" )
    asx  = sorted(asx, key=lambda k: k['last_update'], reverse=True)
    #print asx
    return asx


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
    user_msg_alert  = models.SmallIntegerField(null=True,default=0)
    user_add_alert  = models.SmallIntegerField(null=True,default=0)
    user_not_alert  = models.SmallIntegerField(null=True,default=0)
    def __unicode__(self):
        return str(self.user)
    def fallowers(self):
        a = fallowers.objects.filter(from_user = self).all()
        return a
    def fallwoersCount(self):
        a = fallowers.objects.filter(from_user = self).count()
        return int(a)
    def fallowed(self):
        a = fallowers.objects.filter(to_user = self).all()
        return a
    
    def fallowedCount(self):
        a = fallowers.objects.filter(to_user = self).count()
        return int(a)
    def getStat(self):

        dd = Status.objects.filter(from_user=self)
        cc = dd.count()
        total = 0.0
        
        big = 0.0
        wi = 100.0
        for c in dd.all():
            total = total + c.mood_point
            if big < c.mood_point:
                big = c.mood_point
            if wi > c.mood_point:
                wi =c.mood_point
        try:
            ort = total / cc;
        except:
            ort = 0
        return {"ort":str(ort)[0:3],"big":big,"min":wi,"total":cc}
        
        
    def getSelf(self):
        asx = []
        a = Status.objects.filter(from_user=self).all()
        for z in a:
            
            try:
                ##print findAll(asx,"id",z.post.id)
                st = findAll(asx,"id",z.id)
                ##print str(st)
                kr = int(z.last_update)
                
                
                #print str(st)
                if st == False:
                    u = {"id":z.id,"text":  z.text,"time":z.send_time,"last_update":z.last_update,"from_user":z.from_user,"user":z.from_user,"attachments":z.attachments,"send_time":z.send_time,"mood":z.mood_point,"likes":z.likes(),"comments":z.getCommentsCount()}
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
          
        asx = list()
        for z in a:
            
            try:
                ##print findAll(asx,"id",z.post.id)
                st = findAll(asx,"id",z.post.id)
                #print str(st)
                if st == False:
                    u = {"id":z.post.id,"text":  z.post.text,"time":z.post.send_time,"last_update":z.post.last_update,"from_user":z.post.from_user,"user":z.from_user,"attachments":z.post.attachments,"send_time":z.post.send_time,"mood":z.post.mood_point,"likes":z.post.like_list,"comments":z.post.comment_list}
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
         
        return asx


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
class Status(models.Model):
    from_user       = models.ForeignKey(UserProfiles)
    send_time       = models.IntegerField()
    text            = models.TextField()
    attachments     = models.CharField(max_length=1000)
    mood_point      = models.FloatField()
    last_update     = models.IntegerField()
    like_list       = models.TextField(null=True,default="[]")
    comment_list    = models.TextField(null=True,default="[]")
    
    def saveComment(self,user,text,time):
        import json
        data = json.loads(self.comment_list)
        id = len(data)+13
        data.append({"id":id,"username":str(user.user),"rewrite":user.rewrite,"text":text,"date":time})
        self.comment_list = json.dumps(data)
        self.save()
        k2 = userActions()
        k2.from_user = user
        k2.post = self
        k2.times = time
        k2.post_id = self.id
        k2.save()
        
    def saveLike(self,user):
        import json
        data = json.loads(self.like_list)
        data.append({'username':str(user.user),"rewrite":user.rewrite})
    
    def deleteLike(self,user):
        import json
        data = json.loads(self.like_list)
        tmp_data = []
        save = 0
        for i in data:
            if i.username != str(user.user):
                tmp_data.append(i)
            else:
                save = 1
        if save == 1:
            self.like_list = json.dumps(tmp_data)
            self.save()
    
    def editComment(self,id,user,text):
        import json
        data = json.loads(self.comment_list)
        tmp_data = []
        save = 0
        for i in data:
            if id != i.id:
                tmp_data.append(i)
            else:
                if i.username != str(user.user):
                    tmp_data.append(i)
                else:
                    i.text = text
                    tmp_data.append(i)
                    save = 1
        if save == 1:
            self.comment_list = json.dumps(tmp_data)
            self.save()
      
    def deleteComment(self,id,user):
        import json
        data = json.loads(self.comment_list)
        tmp_data = []
        save = 0
        for i in data:
            if id != i.id:
                tmp_data.append(i)
            else:
                if i.username != str(user.user):
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
    post_id     = models.CharField(null=True,default="",max_length=255)
class myAlerts(models.Model):
    from_user   = models.ForeignKey(UserProfiles)
    post        = models.IntegerField()
    typ         = models.SmallIntegerField()

    
def create_user_profile(sender, instance, created, **kwargs):  
    if created:  
       profile, created = UserProfiles.objects.get_or_create(user=instance)  






post_save.connect(create_user_profile, sender=User) 