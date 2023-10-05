# -*- coding: utf-8 -*-
from django.contrib import admin
from zhongmi.models import *

class ZhongmiCustomerAdmin(admin.ModelAdmin):
    ordering = ('customerid',)
    list_filter = ('gender', 'channelid', 'grade')
    list_display = ('customerid', 'name', 'phone', 'gender', 'age', 'channelid', 'grade', 'saler', 'amount', 'point') 

class ZhongmiChannelAdmin(admin.ModelAdmin):
    ordering = ('channelid',)
    list_display = ('channelid', 'name', 'phone', 'address', 'password')

class ZhongmiItemsAdmin(admin.ModelAdmin):
    ordering = ('itemid',)
    list_display = ('itemid', 'name', 'price')

class ZhongmiSalesAdmin(admin.ModelAdmin):
    ordering = ('salesid',)
    list_display = ('salesid', 'customerid', 'channelid', 'date', 'total')

class ZhongmiSalesdetailAdmin(admin.ModelAdmin):
    ordering = ('detailid',)
    list_display = ('detailid', 'salesid', 'itemid', 'amount')

class ZhongmiShopsAdmin(admin.ModelAdmin):
    ordering = ('grade',)
    list_display = ('grade', 'discount', 'description')

admin.site.register(ZhongmiMain)
admin.site.register(ZhongmiCustomer, ZhongmiCustomerAdmin)
admin.site.register(ZhongmiChannel, ZhongmiChannelAdmin)
admin.site.register(ZhongmiItems, ZhongmiItemsAdmin)
admin.site.register(ZhongmiSales, ZhongmiSalesAdmin)
admin.site.register(ZhongmiSalesdetail, ZhongmiSalesdetailAdmin)
admin.site.register(ZhongmiShops, ZhongmiShopsAdmin)
for r in ZhongmiMain.objects.filter(type=2):
    admin.site.register(eval("Zhongmi"+str(r.id)))
