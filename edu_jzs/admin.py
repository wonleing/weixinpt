# -*e coding: utf-8 -*-
from django.contrib import admin
from edu_jzs.models import *

class EduJzsRecordAdmin(admin.ModelAdmin):
    list_filter = ('type', 'date')
    list_display = ('wxid', 'type', 'date')

class EduJzsMemberAdmin(admin.ModelAdmin):
    list_filter = ('point',)
    list_display = ('wxid', 'name', 'phone', 'point')

class EduJzsPhotoAdmin(admin.ModelAdmin):
    def preview(self, obj):
        return '<img src="%s" width="120" />' % obj.piclink
    preview.short_description = '预览'
    def contact(self, obj):
        ret = EduJzsMember.objects.get(wxid=obj.wxid)
        return '<a href="../edujzsmember/%s/" target="_blank">%s,%s,%s</a>' %(obj.wxid, ret.name, ret.phone, ret.point)
    contact.short_description = '会员信息'
    preview.allow_tags = True
    contact.allow_tags = True
    list_display = ('wxid', 'contact', 'preview')

for i in ("EduJzsEvent", "EduJzsMain", "EduJzsAward", "EduJzs1", "EduJzs2", "EduJzs3", "EduJzs4", "EduJzs5", "EduJzs6", "EduJzs7"):
    admin.site.register(eval(i))
admin.site.register(EduJzsRecord, EduJzsRecordAdmin)
admin.site.register(EduJzsMember, EduJzsMemberAdmin)
admin.site.register(EduJzsPhoto, EduJzsPhotoAdmin)
