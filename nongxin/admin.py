# -*- coding: utf-8 -*-
from django.contrib import admin
from nongxin.models import *

class NongxinPxAdmin(admin.ModelAdmin):
    list_filter = ('method',)
    list_display = ('pxid','pxname','pxtime','description','tip','method','upto','endtime','link')

class NongxinRecordAdmin(admin.ModelAdmin):
    ordering = ('-id',)
    list_filter = ('pxname','status','company','gender','hotel')
    list_display = ('pxname','company','name','gender','race','department','position','contact','phone','arrival','anumber','adate','atime','astation','hotel','status')

admin.site.register(NongxinPx, NongxinPxAdmin)
admin.site.register(NongxinRecord, NongxinRecordAdmin)
