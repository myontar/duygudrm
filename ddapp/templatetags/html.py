# -*- coding: utf-8 -*-
'''
Created on 07.Kas.2010

@author: Administrator
'''
from django.utils.safestring import mark_safe

from django.template import Library
from django.conf import settings
from django.utils.encoding import * 


import json
import re , urllib2
import time
import random

register = Library()






REGEX_YouTube       = "((http:\/\/?(www\.|)+youtube\.com[^\s]*))"
REGEX_YouTube_id    = "(v=[^\s]*)"

REGEX_Google        = "(http:\/\/video\.+google\.com\/[a-zA-Z0-9\.\?\=\&\-\#]+)"
REGEX_GoogleMaps    = "((http:\/\/maps\.google\.com[^\s]*))"

REGEX_Vimeo         = "(http:\/\/(www.|)vimeo.com\/[a-zA-Z0-9\.\?\=\&\-\#\,]+)"
REGEX_Vimeo_id      = "(\/[0-9]+)"

REGEX_DailyMotion   = "(http:\/\/?(www\.|)+dailymotion\.com\/video\/[a-zA-Z0-9\.\-\?\=\&\_\-\#\,]+)"
REGEX_DailyMotion_id= "(video\/[a-zA-Z0-9]+)"

REGEX_Break         = "(http:\/\/(www.|)break.com\/)+((.?)+[a-zA-Z0-9\.\?\=\&\-\#\,]+( |$))"
REGEX_PNG_JPG_GIF   = "(http:\/\/([^\s]+\.(jpg|gif|png)))"
REGEX_AUDIO         = "(http:\/\/|www\.)(.*)\/(.*)(\.mp3|\.m4a)"
REGEX_Izlesene      = "(http:\/\/?(www\.|)+izlesene\.com\/video\/[a-zA-Z0-9\.\-\?\=\&]+)\/([0-9]+)"
REGEX_Tags          = "((#[^\s]*))"


std_headers = {
    'User-Agent': 'Mozilla/5.0 (X11; U; Linux x86_64; en-US; rv:1.9.2.11) Gecko/20101019 Firefox/3.6.11',
    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-us,en;q=0.5',
}
FLV_THM     = [40,40]
IMG_THM     = [40,40]
FLV_SIZE    = [320,240]

try:
    from urlparse import parse_qs
except ImportError:
    from cgi import parse_qs


def GetInHMS(seconds):
    hours = seconds / 3600
    seconds -= 3600*hours
    minutes = seconds / 60
    seconds -= 60*minutes
    return "%02d:%02d:%02d" % (hours, minutes, seconds)


class AutoEmbed():
 
    parse_Text  = None
    def __init__(self,text):
        self.parse_Text = self.remove_html_tags(text)
    
    def remove_html_tags(self,data):
        p = re.compile(r'<.*?>')
        return p.sub('', data)

    def getOnlyLinks(self,providers=[]):
        if len(providers) == 0:
            return self.GrabProviderLinks()
        else:
            result = []
            allproviders = self.GrabProviderLinks()
            for i in providers:
                
                result.append(allproviders[i])
            return result

    def embed(self):

        data = self.getAll()
        for i in data:
                ix = None
                for ix in data[i]:
                        self.parse_Text = self.parse_Text.replace(ix['url'],ix['embed'])
                        #print (ix['url'],ix['embed'])
        return self.parse_Text

        
        
    
    def getAll(self,providers=[]):
        data = self.GrabProviderLinks()
        import urllib

        #Youtube
        youtube = data['youtube']
        print youtube
        youtube_temp = []


        tags = data['tags']
        ttemp = []
        for i in tags:
            print i
            import urllib
            ttemp.append( {"url":i[0],"embed":'<a href="/search?'+urllib.urlencode({"q":i[0]})+'">'+i[0]+'</a>'})
        tags = ttemp
        for i in youtube:
            regex = re.compile(REGEX_YouTube_id)
            id = regex.search(i)
            id = id.group(0).replace("v=","")
            video_info_url = ('http://192.168.1.4/proxy?'+urllib.urlencode({"p":"http://www.youtube.com/get_video_info?&video_id=%s"                      % (id)}))
            print video_info_url
            request = urllib2.Request(video_info_url, None, std_headers)
            video_info_webpage = urllib2.urlopen(request).read()
            video_info = parse_qs(urllib.unquote_plus(video_info_webpage))

            #print video_info
            try:
                info = {}
                info['url'] = i
                info['title'] = video_info['title'][0].replace("ç","c")
                print info['title']
                r = random.randint(1,1123123123123);
                info['thumbnail_url'] = 'imgproxy?'+urllib.urlencode({"p":video_info['thumbnail_url'][0]})
                print info['thumbnail_url']
                info['length_seconds'] = video_info['length_seconds'][0]
                print info['length_seconds']
                info['length'] = GetInHMS(int(video_info['length_seconds'][0]))
                print info['length']
                info['embed'] = u'<div class="embed" id="embed_'+str(r)+'"><a href="javascript:;" onclick="jQuery(\'#embed_'+str(r)+'\').html(w_'+str(r)+');" >'+str(info['title'])+'<br /><img src="'+info['thumbnail_url']+'" align="left" width="60" border=0 onclick="jQuery(\'#embed_'+str(r)+'\').html(w_'+str(r)+');" /><span class="timeinfo">'+info['length']+'</span><script>var w_'+str(r)+' = \'<object width="'+str(FLV_SIZE[0])+'" height="'+str(FLV_SIZE[1])+'"><param name="movie" value="http://www.youtube.com/v/'+id+'"></param><param name="allowFullScreen" value="true"></param><param name="allowscriptaccess" value="always"></param><embed src="http://www.youtube.com/v/'+id+'" type="application/x-shockwave-flash" allowscriptaccess="always" allowfullscreen="true" width="'+str(FLV_SIZE[0])+'" height="'+str(FLV_SIZE[1])+'"></embed></object>\';</script></a><br class="clr" /></div><br class="clr" />'
            #print info['embed']
                youtube_temp.append(info)
            except:
                pass
            
        youtube = youtube_temp

        "http://vimeo.com/api/v2/video/15925400.json"
        vimeo = data['vimeo']
        vimeo_temp = []
        for i in vimeo:
            regex = re.compile(REGEX_Vimeo_id)
            id = regex.search(i)
            id = id.group(0).replace("/","")
            video_info_url = 'http://192.168.1.3/proxy?'+urllib.urlencode({"p":'http://vimeo.com/api/v2/video/%s.json' % id})
            print video_info_url
            request = urllib2.Request(video_info_url, None, std_headers)
            video_info_webpage = urllib2.urlopen(request).read()
            video_info = eval( video_info_webpage)
        #video_info = parse_qs(video_info_webpage)
            info = {}
            r = random.randint(1,1123123123123);

            video_info = video_info[0]
            info['url'] = i
            info['title'] = video_info['title']
            info['thumbnail_url'] = '/imgproxy?'+urllib.urlencode({"p":video_info['thumbnail_large'].replace("\\","")})
            info['length_seconds'] = video_info['duration']
            info['length'] = GetInHMS(int(video_info['duration']))
            info['description'] = video_info['description']
            info['embed'] = u'<div class="embed" id="embed_'+str(r)+'"><a href="javascript:;" onclick="jQuery(\'#embed_'+str(r)+'\').html(w_'+str(r)+');" >'+info['title']+'<br /><img src="'+info['thumbnail_url']+'" align="left" width="60" border=0 onclick="jQuery(\'#embed_'+str(r)+'\').html(w_'+str(r)+');" />'+info['length']+'<script>var w_'+str(r)+' = \'<iframe src="http://player.vimeo.com/video/'+id+'" width="'+str(FLV_SIZE[0])+'" height="'+str(FLV_SIZE[1])+'" frameborder="0"></iframe>\';</script><br class="clr" /><div>'

            info['num_play'] = video_info['stats_number_of_plays']
            vimeo_temp.append(info)
        vimeo = vimeo_temp
        
        
        google = data['google_map']
        google_temp = []
        for i in google:
            print i
            google_temp.append({"embed":'<iframe width="'+str(FLV_SIZE[0])+'" height="'+str(FLV_SIZE[1])+'" frameborder="0" src="'+i+'&output=embed&source=embed"></iframe>',"url":i})
        google =  google_temp
        
        
        dailymotion = data['dailymotion']
        dailymotion_tmp = []
        for i in dailymotion:
            regex = re.compile(REGEX_DailyMotion_id,re.MULTILINE)
            id = regex.search(i)
            id = id.group(0).replace("video/","")

            request = urllib2.Request(i, None, std_headers)
            video_info_webpage = urllib2.urlopen(request).read()
            datav = video_info_webpage.split("<!--")[1].split("-->")[0]
            video_info = {}
            for ix in datav.split("<Attribute"):
                
                if ix.find("Attribute") > -1:
                        key = ix.split('\Attribute')[0].split("name=")[1].split('"')[1]
                        
                        val = ix.split('\Attribute')[0].split(">")[1].split('<')[0]
                        video_info[key] = val

            info = {}
            info['url'] = i
            info['title'] = video_info['title']
            info['thumbnail_url'] = "http://www.dailymotion.com/thumbnail/160x120/video/%s_" % id
            info['length_seconds'] = video_info['duration']
            info['length'] = GetInHMS(int(video_info['duration']))
            info['num_play'] = video_info['views']
            
            info['embed'] = """<span>
                                    <img src="" style="cursor:pointer;"/>
                                    <div style="display:none;"><object width="560" height="315">
                                    <param name="movie" value="http://www.dailymotion.com/swf/video/%s"></param>
                                    <param name="allowFullScreen" value="true"></param>
                                    <param name="allowScriptAccess" value="always"></param>
                                    <embed type="application/x-shockwave-flash" src="http://www.dailymotion.com/swf/video/%s" width="560" height="315" allowfullscreen="true" allowscriptaccess="always"></embed>
                                </object></div></span>""" % (id,id)
            dailymotion_tmp.append(info)

        dailymotion = dailymotion_tmp



        
        image = data['images']
        image_tmp = []
        for i in image:
                image_tmp.append({'embed':'<div class="embed"><img src="'+i+'" /><br class="clr" /></div> ',"url":i})
        image = image_tmp
        
        all = {"images":image,"gmap":google,'dailymotion':dailymotion,'vimeo':vimeo,"youtube":youtube,"tags":tags}
        return all

    def clear(self,arr):
        tmp = []
        for i in arr:
            if i[0] != None:
                tmp.append(i[0])
        return tmp
        
    def GrabProviderLinks(self):
        regex = re.compile(REGEX_YouTube)
        youtube = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_Google)
        google = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_GoogleMaps)
        googlemap = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_Vimeo)
        vimeo = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_Break)
        break_ = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_PNG_JPG_GIF)
        images = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_AUDIO)
        audio = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_DailyMotion)
        dailymotion = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_Izlesene)
        izlesene = regex.findall(self.parse_Text)

        regex = re.compile(REGEX_Tags)
        tags = regex.findall(self.parse_Text)

        images = self.clear(images)
        izlesene = self.clear(izlesene)
        youtube = self.clear(youtube)
        googlemap = self.clear(googlemap)
        vimeo = self.clear(vimeo)
        break_ = self.clear(break_)
        audio = self.clear(audio)
        dailymotion = self.clear(dailymotion)
        
        
        return {"tags":tags,"dailymotion":dailymotion,"google":google,"youtube":youtube,"break":break_,"google_map":googlemap,"vimeo":vimeo,"images":images,"audio":audio,"izlesene":izlesene}
    

        
        


@register.filter
def phtml(text):
    
    
    embed = AutoEmbed(text)
    #print embed.GrabProviderLinks() 
    return mark_safe(embed.embed())
register.filter('phtml', phtml)
phtml.is_safe = True
