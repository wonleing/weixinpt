# -*- coding: utf-8 -*-
from django.contrib import admin
from dfth.models import *

class DfthSourceAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('sourcename', 'number', 'type')

class DfthProductAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('productname', 'number', 'type')

class DfthSupplyerAdmin(admin.ModelAdmin):
    list_display = ('supplyername', 'address', 'phone')

class DfthCustomerAdmin(admin.ModelAdmin):
    list_filter = ('type', 'district', 'location')
    list_display = ('customername', 'type', 'district', 'location', 'contact', 'phone', 'address', 'invoiceinfo') 

class DfthEmployeeAdmin(admin.ModelAdmin):
    list_filter = ('position', 'auth')
    list_display = ('employeename', 'position', 'phone', 'password', 'auth') 

class DfthContractAdmin(admin.ModelAdmin):
    ordering = ('-date',)
    list_filter = ('customername',)
    list_display = ('contractid', 'customername', 'summary', 'total', 'dater') 
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthPurchaseAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_filter = ('supplyername', 'sourcename')
    list_display = ('supplyername', 'sourcename', 'number', 'price', 'dater', 'keepdate', 'location')
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthConsumeAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_filter = ('employeename', 'sourcename')
    list_display = ('employeename', 'sourcename', 'number', 'dater')
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthProduceAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_filter = ('productname',)
    list_display = ('productname', 'number', 'dater', 'keepdate')
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthSaleAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_filter = ('productname', 'customername')
    list_display = ('productname', 'customername', 'contractid', 'number', 'dater', 'keepdate', 'price')
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthIncomeAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_filter = ('contractid', 'customername')
    list_display = ('contractid', 'customername', 'number', 'dater')
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthExpenseAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_filter = ('username', 'type', 'status')
    list_display = ('username', 'type', 'reason', 'number', 'dater', 'status')
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthNoticeAdmin(admin.ModelAdmin):
    list_filter = ('status',)
    list_display = ('text', 'dater', 'status')
    def dater(self,obj):
        return obj.date.strftime("%Y%m%d")
    dater.short_description = "更新日期"

class DfthDeviceAdmin(admin.ModelAdmin):
    list_display = ('deviceid', 'devicename', 'buydate', 'price')

admin.site.register(DfthSource, DfthSourceAdmin)
admin.site.register(DfthProduct, DfthProductAdmin)
admin.site.register(DfthSupplyer, DfthSupplyerAdmin)
admin.site.register(DfthCustomer, DfthCustomerAdmin)
admin.site.register(DfthEmployee, DfthEmployeeAdmin)
admin.site.register(DfthContract, DfthContractAdmin)
admin.site.register(DfthPurchase, DfthPurchaseAdmin)
admin.site.register(DfthConsume, DfthConsumeAdmin)
admin.site.register(DfthProduce, DfthProduceAdmin)
admin.site.register(DfthSale, DfthSaleAdmin)
admin.site.register(DfthIncome, DfthIncomeAdmin)
admin.site.register(DfthExpense, DfthExpenseAdmin)
admin.site.register(DfthNotice, DfthNoticeAdmin)
admin.site.register(DfthDevice, DfthDeviceAdmin)
