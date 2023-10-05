# -*- coding: utf-8 -*-
from django.contrib import admin
from yukangyuan.models import *

class YukangyuanProductAdmin(admin.ModelAdmin):
    ordering = ('productid',)
    list_filter = ('type', 'brand', 'flag')
    list_display = ('productid', 'code', 'name', 'type', 'brand', 'storage', 'flag', 'price1', 'price2', 'price3')

class YukangyuanSalerAdmin(admin.ModelAdmin):
    ordering = ('salerid',)
    list_display = ('salerid', 'name', 'description')

class YukangyuanCustomerAdmin(admin.ModelAdmin):
    ordering = ('customerid',)
    list_filter = ('salerid', 'privilege', 'grade')
    list_display = ('customerid', 'name', 'contact', 'phone', 'address', 'salerid', 'privilege', 'grade') 

class YukangyuanOrderAdmin(admin.ModelAdmin):
    ordering = ('-orderid',)
    def cname(self, obj):
        return YukangyuanCustomer.objects.get(customerid=obj.customerid).name
    cname.short_description = '客户名称'
    def sname(self, obj):
        return YukangyuanSaler.objects.get(salerid=YukangyuanCustomer.objects.get(customerid=obj.customerid).salerid).name
    sname.short_description = '业务员'
    def odetail(self, obj):
        return '<a href="/yukangyuan/getdetail/?orderid=%s&html=1" target="_blank">订单详情</a>' %obj.orderid
    odetail.short_description = '订单详情'
    odetail.allow_tags = True
    list_filter = ('status', 'date')
    list_display = ('orderid', 'cname', 'sname', 'date', 'total', 'status', 'odetail')

class YukangyuanOrderdetailAdmin(admin.ModelAdmin):
    ordering = ('-detailid',)
    list_filter = ('status', 'date')
    list_display = ('detailid', 'orderid', 'customerid', 'productid', 'amount', 'total', 'status', 'date')

class YukangyuanSupportAdmin(admin.ModelAdmin):
    ordering = ('-supportid',)
    def cname(self, obj):
        return YukangyuanCustomer.objects.get(customerid=obj.customerid).name
    cname.short_description = '客户名称'
    def sname(self, obj):
        return YukangyuanSaler.objects.get(salerid=YukangyuanCustomer.objects.get(customerid=obj.customerid).salerid).name
    sname.short_description = '业务员'
    list_filter = ('customerid', 'date')
    list_display = ('supportid', 'cname', 'sname', 'reason', 'detail', 'total', 'date')

class YukangyuanReportAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    def sname(self, obj):
        return YukangyuanSaler.objects.get(salerid=obj.salerid).name
    sname.short_description = '业务员'
    list_filter = ('salerid', 'date')
    list_display = ('reportid', 'sname', 'content', 'date')

class YukangyuanReturnAdmin(admin.ModelAdmin):
    ordering = ('-returnid',)
    def cname(self, obj):
        return YukangyuanCustomer.objects.get(customerid=obj.customerid).name
    cname.short_description = '客户名称'
    def sname(self, obj):
        return YukangyuanSaler.objects.get(salerid=YukangyuanCustomer.objects.get(customerid=obj.customerid).salerid).name
    sname.short_description = '业务员'
    list_filter = ('customerid', 'date')
    list_display = ('returnid', 'cname', 'sname', 'detail', 'reason', 'total', 'date')

admin.site.register(YukangyuanProduct, YukangyuanProductAdmin)
admin.site.register(YukangyuanSaler, YukangyuanSalerAdmin)
admin.site.register(YukangyuanCustomer, YukangyuanCustomerAdmin)
admin.site.register(YukangyuanOrder, YukangyuanOrderAdmin)
admin.site.register(YukangyuanOrderdetail, YukangyuanOrderdetailAdmin)
admin.site.register(YukangyuanSupport, YukangyuanSupportAdmin)
admin.site.register(YukangyuanReport, YukangyuanReportAdmin)
admin.site.register(YukangyuanReturn, YukangyuanReturnAdmin)
