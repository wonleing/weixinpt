# -*- coding: utf-8 -*-
from django.contrib import admin
from bg_xb.models import *

class BgXbMemberAdmin(admin.ModelAdmin):
    ordering = ('memberid',)
    list_filter = ('level',)
    list_display = ('memberid', 'name', 'detail', 'address', 'phone', 'contact', 'level')

class BgXbProductAdmin(admin.ModelAdmin):
    ordering = ('productid',)
    list_filter = ('member', 'tag', 'onsale')
    list_display = ('productid', 'member', 'level', 'type', 'title', 'description', 'price', 'tag', 'onsale')

class BgXbUserAdmin(admin.ModelAdmin):
    ordering = ('userid',)
    list_filter = ('level',)
    list_display = ('userid', 'name', 'detail', 'address', 'total', 'level')

class BgXbMainAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('id', 'title', 'description', 'pic', 'link', 'type')

class BgXbQaAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')

class BgXbRecordAdmin(admin.ModelAdmin):
    list_display = ('otid', 'userid', 'productid', 'detail', 'number', 'total', 'status', 'date', 'kdcom', 'kdnu')
    list_filter = ('status', 'kdcom', 'date')

class BgXb1Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'title', 'price', 'description')

class BgXb2Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'title', 'price', 'description')
    
class BgXb3Admin(admin.ModelAdmin):
    ordering = ('id',)
    list_display = ('id', 'title', 'price', 'description')
    
admin.site.register(BgXb1, BgXb1Admin)
admin.site.register(BgXb2, BgXb2Admin)
admin.site.register(BgXb3, BgXb3Admin)
admin.site.register(BgXbMember, BgXbMemberAdmin)
admin.site.register(BgXbUser, BgXbUserAdmin)
admin.site.register(BgXbProduct, BgXbProductAdmin)
admin.site.register(BgXbColmember)
admin.site.register(BgXbColproduct)
admin.site.register(BgXbMain, BgXbMainAdmin)
admin.site.register(BgXbQa, BgXbQaAdmin)
admin.site.register(BgXbRecord, BgXbRecordAdmin)
