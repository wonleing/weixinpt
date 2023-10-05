# -*- coding: utf-8 -*-
from django.contrib import admin
from mygym.models import *

class MygymCustomerAdmin(admin.ModelAdmin):
    ordering = ('cid',)
    list_filter = ('sid',)
    list_display = ('cid', 'name', 'phone', 'sid') 

class MygymSiteAdmin(admin.ModelAdmin):
    ordering = ('sid',)
    list_display = ('sid', 'name', 'phone')

admin.site.register(MygymMain)
admin.site.register(MygymCustomer, MygymCustomerAdmin)
admin.site.register(MygymSite, MygymSiteAdmin)
for r in MygymMain.objects.filter(type=2):
    admin.site.register(eval("Mygym"+str(r.id)))
