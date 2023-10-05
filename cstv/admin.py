# -*- coding: utf-8 -*-
from django.contrib import admin
from cstv.models import *
class CstvVideosAdmin(admin.ModelAdmin):
    list_filter = ('tag', 'update')
    def dater(self,obj):
        return obj.update.strftime("%Y-%m-%d %H:%M")
    dater.short_description = "更新日期"
    list_display = ('video_id', 'title', 'description', 'tag', 'dater')
    ordering = ('-update',)
class CstvSettingsAdmin(admin.ModelAdmin):
    list_display = ('key', 'value')

admin.site.register(CstvVideos, CstvVideosAdmin)
admin.site.register(CstvSettings, CstvSettingsAdmin)
