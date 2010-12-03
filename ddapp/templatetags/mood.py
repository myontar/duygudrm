'''
Created on 06.Kas.2010

@author: Administrator
'''
# -*- coding: utf-8 -*-

from django.template import Library
from django.conf import settings

import time


register = Library()





@register.filter
def mood(tim):
    
    r = 255
    g = 255

    print "tim tim tim"
    print float(tim)
    #if type(tim) == type("str"):
    #    tim = float(tim)
    if tim > 5.0:
        
        p = (5.0-tim) / (5.0 / 100.0)
        r =  int((255.0 / 100.0) * p)
        
    if tim < 5.0:
        p =  tim / (5.0 / 100.0)
        g =  int((255.0 / 100.0) * p)
    html = '<div class="mood" style="background-color:rgb('+str(r)+','+str(g)+',50)">'+str(tim)+'</div>'
    return html
    
register.filter('mood', mood)