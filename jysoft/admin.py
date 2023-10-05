# -*- coding: utf-8 -*-
from django.contrib import admin
from jysoft.models import *

class JysoftContractAdmin(admin.ModelAdmin):
    list_display = ('client', 'amount', 'pname', 'contact', 'phone', 'starttime', 'nexttime', 'seller')
    list_filter = ('pname','seller','starttime')

class JysoftFinanceAdmin(admin.ModelAdmin):
    list_display = ('type', 'year', 'month', 'day', 'summary', 'amount', 'user', 'message', 'date')
    list_filter = ('type', 'year', 'month', 'user')

class JysoftMiaochunAdmin(admin.ModelAdmin):
    list_display = ('type', 'year', 'month', 'day', 'summary', 'amount', 'user', 'message', 'date')
    list_filter = ('type', 'year', 'month', 'user')

admin.site.register(JysoftContract, JysoftContractAdmin)
admin.site.register(JysoftFinance, JysoftFinanceAdmin)
admin.site.register(JysoftMiaochun, JysoftMiaochunAdmin)
