# -*e coding: utf-8 -*-
from django.contrib import admin
from wanda.models import *

class WandaRecordAdmin(admin.ModelAdmin):
    list_filter = ('type','shareid')
    list_display = ('orderid', 'wxid', 'shareid', 'type', 'date')

class WandaMemberAdmin(admin.ModelAdmin):
    list_display = ('wxid', 'name', 'phone', 'point')

class WandaPhotoAdmin(admin.ModelAdmin):
    def preview(self, obj):
        return '<img src="%s" width="120" />' % obj.piclink
    preview.short_description = '预览'
    def contact(self, obj):
        ret = WandaMember.objects.get(wxid=obj.wxid)
        return '<a href="../wandamember/%s/" target="_blank">%s,%s,%s</a>' %(obj.wxid, ret.name, ret.phone, ret.point)
    contact.short_description = '会员信息'
    preview.allow_tags = True
    contact.allow_tags = True
    list_display = ('wxid', 'contact', 'preview')

for i in ("WandaEvent", "WandaMain", "WandaAward", "Wanda1", "Wanda2", "Wanda3"):
    admin.site.register(eval(i))
admin.site.register(WandaRecord, WandaRecordAdmin)
admin.site.register(WandaMember, WandaMemberAdmin)
admin.site.register(WandaPhoto, WandaPhotoAdmin)
