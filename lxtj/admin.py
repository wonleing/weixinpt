# -*- coding: utf-8 -*-
from django.contrib import admin
from lxtj.models import *

class LxtjChargeAdmin(admin.ModelAdmin):
    list_filter = ('active',)
    list_display = ('cpid', 'operationid', 'title', 'price', 'active')
    def active_tag(self, request, queryset):
        rows_updated = queryset.update(active=1)
        self.message_user(request, "%s个热词启用成功" % rows_updated)
    def deactive_tag(self, request, queryset):
        rows_updated = queryset.update(active=0)
        self.message_user(request, "%s个热词关闭成功" % rows_updated)
    active_tag.short_description = "启用热词"
    deactive_tag.short_description = "关闭热词"
    actions = [active_tag, deactive_tag]

class LxtjLgAdmin(admin.ModelAdmin):
    list_filter = ('cateid',)
    list_display = ('cateid', 'title')

class LxtjFreeAdmin(admin.ModelAdmin):
    list_filter = ('cateid',)
    list_display = ('cateid', 'title')

admin.site.register(LxtjCharge, LxtjChargeAdmin)
admin.site.register(LxtjLg, LxtjLgAdmin)
admin.site.register(LxtjFree, LxtjFreeAdmin)
for i in ("LxtjMember","LxtjMain", "LxtjPayment"):
    admin.site.register(eval(i))
