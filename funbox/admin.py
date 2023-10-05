# -*e coding: utf-8 -*-
from django.contrib import admin
from funbox.models import *
class FunboxMsgAdmin(admin.ModelAdmin):
    list_filter = ('memberid', 'status')
    list_display = ('memberid', 'amount', 'accountinfo', 'date', 'status')

class FunboxRecordAdmin(admin.ModelAdmin):
    list_filter = ('memberid', 'type', 'status')
    list_display = ('memberid', 'type', 'detail', 'amount', 'date', 'status')
    ordering = ('-date',)

class FunboxMemberAdmin(admin.ModelAdmin):
    list_filter = ('memberid', 'type', 'fromagent')
    list_display = ('memberid', 'type', 'name', 'phone', 'balance', 'total', 'fromagent', 'jointime')

class FunboxUserAdmin(admin.ModelAdmin):
    list_filter = ('type',)
    list_display = ('userid', 'type', 'name', 'phone', 'balance', 'total', 'jointime')

class FunboxCommentAdmin(admin.ModelAdmin):
    list_filter = ('memberid', 'status', 'tip')
    list_display = ('commentid', 'memberid', 'userid', 'status', 'tip', 'date')

admin.site.register(FunboxRecord, FunboxRecordAdmin)
admin.site.register(FunboxMember, FunboxMemberAdmin)
admin.site.register(FunboxMsg, FunboxMsgAdmin)
admin.site.register(FunboxUser, FunboxUserAdmin)
admin.site.register(FunboxComment, FunboxCommentAdmin)
