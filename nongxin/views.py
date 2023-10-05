# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from nongxin.models import *
import datetime

def baoming(request):
    pxid = request.GET.get('pxid')
    if not pxid:
        return render(request, 'nongxinlist.html', {'pxlist':NongxinPx.objects.all()})
    try:
        px = NongxinPx.objects.get(pxid=pxid)
    except:
        return HttpResponse('<h1>无此培训项目</h1>')
    endtime = px.endtime.strftime("%Y-%m-%d %H:%M")
    context = {'pxid':px.pxid,'pxname':px.pxname,'pxtime':px.pxtime,'description':px.description,'tip':px.tip,'upto':px.upto,'endtime':endtime,'link':px.link}
    return render(request, 'nongxin.html', context)

@csrf_exempt
def add(request):
    pxname = request.POST.get('pxname')
    company = request.POST.get('company')
    if request.POST.get('othercompany'):
        company = request.POST.get('othercompany')
    name = request.POST.get('name')
    gender = request.POST.get('gender')
    race = request.POST.get('race')
    department = request.POST.get('department')
    position = request.POST.get('position')
    contact = request.POST.get('contact')
    phone = request.POST.get('phone')
    arrival = request.POST.get('arrival')
    anumber = request.POST.get('anumber')
    adate = request.POST.get('adate')
    atime = request.POST.get('atime')
    astation = request.POST.get('astation')
    hotel = request.POST.get('hotel')
    comment = request.POST.get('comment')
    ret = NongxinRecord.objects.filter(pxname=pxname,company=company,name=name)
    if ret:
        ret[0].arrival = arrival
        ret[0].anumber = anumber
        ret[0].adate = adate
        ret[0].atime = atime
        ret[0].astation = astation
        ret[0].comment = comment
        ret[0].save()
        return HttpResponse('<html><h1>信息更新成功</h1><script>setTimeout("window.history.go(-1)",2000)</script></html><html>')
    px = NongxinPx.objects.get(pxname=pxname)
    if pxname == "" or company == u"请选择" or name == "" or gender == u"请选择" or hotel == u"请选择":
        return HttpResponse('<html><h1 style="font-size:5em;height:100%;display:flex;align-items:center;">提交失败，报名信息必须填写完整</h1><script>setTimeout("window.history.go(-1)",2000)</script></html>')
    elif len(NongxinRecord.objects.filter(pxname=pxname)) < px.upto and px.endtime > datetime.datetime.now():
        NongxinRecord(pxname=pxname,company=company,name=name,gender=gender,race=race,department=department,position=position,contact=contact,phone=phone,arrival=arrival,anumber=anumber,adate=adate,atime=atime,astation=astation,hotel=hotel,comment=comment,status=0).save()
        return HttpResponse('<html><head><meta http-equiv="refresh" content="2;url=../?pxid='+request.POST.get('pxid')+u'"></head><h1 style="font-size:5em;height:100%;display:flex;align-items:center;">提交成功，页面跳转后填写同行人员信息</h1></html><html>')
    else:
        return HttpResponse('<html><h1 style="font-size:5em;height:100%;display:flex;align-items:center;">报名已截止，请等待下次培训</h1></html>')
