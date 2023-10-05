# -*- coding: utf-8 -*-
from django.contrib import admin
from __pname__.models import *

for i in ("__Pname__Msg", "__Pname__Main","__Pname__1","__Pname__2","__Pname__3","__Pname__4","__Pname__5","__Pname__6","__Pname__7"):
    admin.site.register(eval(i))
