# -*- coding: utf-8 -*-

from django.template import Library
from django.conf import settings
from django.utils.translation import ugettext as _

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
    month = [_("Ocak"),_("Subat"),_("Mart"),_("Nisan"),_("Mayis"),_("Haziran"),_("Temmuz"),_("Agustos"),_("Eylul"),_("Ekim"),_("Kasim"),_("Aralik")]
    days = [_('Pazartesi'),_("Sali"),_("Carsamba"),_("Persembe"),_("Cuma")]
    rtmhour = real.tm_hour
    if len(str(real.tm_hour)) == 1:
        rtmhour = "0"+str(real.tm_hour)
    rtmnim = real.tm_min
    if len(str(real.tm_min)) == 1:
        rtmnim = "0"+str(real.tm_min)
    if now.tm_mon == real.tm_mon:
        if now.tm_mday == real.tm_mday:
            if tm_hour == rtmhour:
                if now.tm_min == rtmnim:
                    text = _("Bir kac saniye once")
                else:
                    text = _("%(dakika)s dakika once") % {"dakika":now.tm_min - int(rtmnim)}
            else:
                text = _("%(saat)s saat once") % {"saat":str(tm_hour - int(rtmhour))}
        else:
           if now.tm_mday - real.tm_mday < 2:
               text = _("Dun %(saat)s") % {"saat":str(rtmhour)+":"+str(rtmnim)}
           elif now.tm_mday - real.tm_mday < 7 and real.tm_wday < now.tm_wday:
               text = _("Gecen Hafta %(gun)s %(saat)s") % {"gun":days[real.tm_wday],"saat":str(rtmhour)+":"+str(rtmnim)}
           elif now.tm_mday - real.tm_mday < 7:
               
               text = _("%(gun)d Gun once %(saat)s") % {"gun": now.tm_mday - real.tm_mday,"saat" : str(rtmhour)+":"+str(rtmnim)}
               #text = ""
           elif now.tm_mday - real.tm_mday > 13:
               text = "%d %s %s" % (now.tm_mday - real.tm_mday,month[real.tm_mon-1],str(rtmhour)+":"+str(rtmnim))
         
    else:
        text = "%d %s %s" % (real.tm_mday,month[real.tm_mon-1],str(rtmhour)+":"+str(rtmnim))
    
    return text
    
register.filter('tdate', tdate)
