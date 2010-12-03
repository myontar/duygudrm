# -*- coding: utf-8 -*-

from django.template import Library
from django.conf import settings

import time


register = Library()





@register.filter
def tdate(tim):
    now = time.localtime()
    tm_hour = now.tm_hour + 1
    if type(tim) == type("str"):
        if tim != "":
            tim = int(tim)
        else:
            tim = 1289068211.0
    tim = tim + 3600
    #print "tim geldi" 
    #print tim 
    if tim == None or tim == "":
        tim = 1289068211.0
    real = time.localtime(float(tim))
    text = ""
    month = ["Ocak","Subat","Mart","Nisan","Mayis","Haziran","Temmuz","Agustos","Eylul","Ekim","Kasim","Aralik"]
    days = ['Pazartesi',"Sali","Carsamba","Persembe","Cuma"]
    if now.tm_mon == real.tm_mon:
        if now.tm_mday == real.tm_mday:
            if tm_hour == real.tm_hour:
                if now.tm_min == real.tm_min:
                    text = "Bir kac saniye once"
                else:
                    text = "%d dakika once" % (now.tm_min - real.tm_min)
            else:
                text = "%d saat once" % (tm_hour - real.tm_hour)
        else:
           if now.tm_mday - real.tm_mday < 2:
               text = "Dun %s" % (str(real.tm_hour)+":"+str(real.tm_min))
           elif now.tm_mday - real.tm_mday < 7 and real.tm_wday < now.tm_wday:
               text = "%Gecen Hafta %s %s" % (now.tm_mday - real.tm_mday,days[real.tm_wday],str(real.tm_hour)+":"+str(real.tm_min))
           elif now.tm_mday - real.tm_mday < 7:
               
               text = "%d Gun once %s" % (now.tm_mday - real.tm_mday,str(real.tm_hour)+":"+str(real.tm_min))
               
           elif now.tm_mday - real.tm_mday > 13:
               text = "%d %s %s" % (now.tm_mday - real.tm_mday,month[real.tm_mon],str(real.tm_hour)+":"+str(real.tm_min))
        
    else:
        text = "%d %s %s" % (now.tm_mday - real.tm_mday,month[real.tm_mon],str(real.tm_hour)+":"+str(real.tm_min))
    
    return text
    
register.filter('tdate', tdate)