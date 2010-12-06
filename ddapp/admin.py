'''
Created on 04.Kas.2010

@author: Administrator
'''

from duygudrm.ddapp.models import UserProfiles,UserMessages,Status,fallowers,userActions , Likes , userLoginService
from django.contrib import admin


admin.site.register(UserProfiles)
admin.site.register(userLoginService)
admin.site.register(Status)
admin.site.register(UserMessages)
admin.site.register(fallowers)
admin.site.register(Likes)
admin.site.register(userActions)
