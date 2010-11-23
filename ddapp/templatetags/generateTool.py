'''
Created on 10.Kas.2010

@author: Administrator
'''
from django.template import Library
from django.conf import settings

import time


register = Library()
import json
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

    
    