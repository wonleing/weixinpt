# -*- coding: utf-8 -*-
from django.contrib import admin
from live_hk.models import *

class LiveHkRecordAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('name', 'phone', 'type', 'date')

class LiveHkMemberAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('name', 'phone', 'wxid', 'company', 'job', 'type', 'point')

for i in ("LiveHkTopic","LiveHkMain", "LiveHkAward"):
    admin.site.register(eval(i))
admin.site.register(LiveHkRecord, LiveHkRecordAdmin)
admin.site.register(LiveHkMember, LiveHkMemberAdmin)
