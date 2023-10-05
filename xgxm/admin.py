# -*- coding: utf-8 -*-
from django.contrib import admin
from xgxm.models import *

class XgxmMemberAdmin(admin.ModelAdmin):
    ordering = ('memberid',)
    list_filter = ('level',)
    list_display = ('memberid', 'name', 'detail', 'address', 'phone', 'contact', 'level')

class XgxmProductAdmin(admin.ModelAdmin):
    ordering = ('productid',)
    list_filter = ('tag', 'onsale')
    list_display = ('productid', 'level', 'type', 'title', 'description', 'price', 'tag', 'onsale')

class XgxmUserAdmin(admin.ModelAdmin):
    ordering = ('userid',)
    list_filter = ('level',)
    list_display = ('userid', 'name', 'detail', 'address', 'total', 'level')

class XgxmMainAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('id', 'title', 'pic', 'type')

class XgxmQaAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')

class XgxmRecordAdmin(admin.ModelAdmin):
    list_display = ('otid', 'userid', 'productid', 'detail', 'number', 'total', 'status', 'date', 'kdcom', 'kdnu')
    list_filter = ('status', 'kdcom', 'date')

admin.site.register(XgxmMember, XgxmMemberAdmin)
admin.site.register(XgxmUser, XgxmUserAdmin)
admin.site.register(XgxmProduct, XgxmProductAdmin)
admin.site.register(XgxmColproduct)
admin.site.register(XgxmMain, XgxmMainAdmin)
admin.site.register(XgxmQa, XgxmQaAdmin)
admin.site.register(XgxmRecord, XgxmRecordAdmin)
