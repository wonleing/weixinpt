# -*- coding: utf-8 -*-
from django.contrib import admin
from taobao_hxf.models import *

for i in ("TaobaoHxfMsg", "TaobaoHxfMain","TaobaoHxf1","TaobaoHxf2","TaobaoHxf3","TaobaoHxf4","TaobaoHxf5","TaobaoHxf6","TaobaoHxf7"):
    admin.site.register(eval(i))
