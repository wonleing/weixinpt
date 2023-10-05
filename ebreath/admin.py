# -*- coding: utf-8 -*-
from django.contrib import admin
from ebreath.models import *

class EbreathMemberAdmin(admin.ModelAdmin):
    ordering = ('memberid',)
    list_filter = ('level',)
    list_display = ('memberid', 'name', 'detail', 'phone', 'level')

class EbreathProductAdmin(admin.ModelAdmin):
    ordering = ('productid',)
    list_filter = ('tag', 'onsale')
    list_display = ('productid', 'title', 'description', 'price', 'origprice', 'tag', 'style', 'onsale', 'number')

class EbreathUserAdmin(admin.ModelAdmin):
    ordering = ('userid',)
    list_filter = ('level',)
    list_display = ('userid', 'name', 'detail', 'address', 'total', 'balance', 'level')

class EbreathPayAdmin(admin.ModelAdmin): 
    ordering = ('-date',)
    def cname(self, obj):
        return EbreathUser.objects.get(userid=obj.userid).name
    cname.short_description = '充值人'
    def dater(self,obj):
        return obj.date.strftime("%Y-%m-%d %H:%M")
    dater.short_description = "更新日期"
    list_filter = ('date', 'amount',)
    list_display = ('otid', 'userid', 'cname', 'memberid', 'amount', 'dater')

class EbreathRecordAdmin(admin.ModelAdmin): 
    readonly_fields = ('userid', 'productid', 'number', 'total')
    ordering = ('-recordid',)
    def cname(self, obj):
        return EbreathUser.objects.get(userid=obj.userid).name
    cname.short_description = '下单用户'
    def pname(self, obj):
        return EbreathProduct.objects.get(productid=obj.productid).title
    pname.short_description = '下单商品'
    def dater(self,obj):
        return obj.date.strftime("%Y-%m-%d %H:%M")
    dater.short_description = "更新日期"
    search_fields = ('recname', 'rectel', 'total')
    list_display = ('recordid', 'cname', 'pname', 'number', 'total', 'recname', 'rectel', 'province', 'city', 'county', 'detail', 'status', 'dater', 'kdcom', 'kdnu')
    list_filter = ('province', 'city', 'county', 'status', 'productid', 'kdcom', 'date')

class EbreathQaAdmin(admin.ModelAdmin):
    list_display = ('question', 'answer')

class EbreathCommentAdmin(admin.ModelAdmin):
    list_display = ('userid', 'productid', 'name', 'detail', 'isshow')

class EbreathSettingAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('id', 'title', 'description', 'pic', 'type')

admin.site.register(EbreathMember, EbreathMemberAdmin)
admin.site.register(EbreathProduct, EbreathProductAdmin)
admin.site.register(EbreathUser, EbreathUserAdmin)
admin.site.register(EbreathPay, EbreathPayAdmin)
admin.site.register(EbreathRecord, EbreathRecordAdmin)
admin.site.register(EbreathQa, EbreathQaAdmin)
admin.site.register(EbreathComment, EbreathCommentAdmin)
admin.site.register(EbreathSetting, EbreathSettingAdmin)
