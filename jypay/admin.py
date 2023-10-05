# -*e coding: utf-8 -*-
from django.contrib import admin
from jypay.models import *
class JypayMsgAdmin(admin.ModelAdmin):
    list_filter = ('centerid', 'memberid')
    list_display = ('centerid', 'memberid', 'amount', 'accountinfo', 'date')

class JypayRecordAdmin(admin.ModelAdmin):
    list_filter = ('memberid', 'type', 'status', 'date')
    list_display = ('memberid', 'type', 'detail', 'amount', 'date', 'status')
    ordering = ('-date',)

class JypayCenterAdmin(admin.ModelAdmin):
    list_filter = ('limit',)
    list_display = ('centerid', 'limit', 'name', 'phone', 'balance', 'total', 'man', 'jian', 'endtime')

class JypayMemberAdmin(admin.ModelAdmin):
    list_filter = ('type', 'fromagent')
    list_display = ('memberid', 'type', 'name', 'phone', 'balance', 'total', 'fromagent', 'jointime')

class JypayUserAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('userid', 'type', 'name', 'phone', 'balance', 'total', 'jointime')

class JypayCommentAdmin(admin.ModelAdmin):
    list_filter = ('memberid', 'status', 'tip')
    list_display = ('commentid', 'memberid', 'userid', 'status', 'tip', 'date')

admin.site.register(JypayMsg, JypayMsgAdmin)
admin.site.register(JypayRecord, JypayRecordAdmin)
admin.site.register(JypayCenter, JypayCenterAdmin)
admin.site.register(JypayMember, JypayMemberAdmin)
admin.site.register(JypayUser, JypayUserAdmin)
admin.site.register(JypayComment, JypayCommentAdmin)
