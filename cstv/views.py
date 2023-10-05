# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render
from cstv.models import *
serverIP = 'http://api.cstv.hiveview.com:81/'
from django.core import serializers
from django.db.models import Sum

def videolist(request):
    #tag = request.GET.get('tag')
    #tags = CstvVideos.objects.values_list('tag', flat=True).distinct()
    videos = CstvVideos.objects.all().order_by('-update')[:50]
    #context = { 'videos':serializers.serialize("json", videos) }
    banner = CstvSettings.objects.get(key='banner').value
    title = CstvSettings.objects.get(key='title').value
    total = CstvVideos.objects.aggregate(Sum('description'))
    context = { 'videos': videos, 'banner':banner, 'title':title, 'total':total }
    return render(request, 'cstv/list.html', context)

def topiclist(request):
    tag = request.GET.get('tag')
    context = { 'tag': tag }
    return render(request, 'cstv/list2.html', context)

def videoplay(request):
    video_id = request.GET.get('video_id')
    video  = CstvVideos.objects.get(video_id=video_id)
    video.description = video.description+1
    video.save()
    banner = CstvSettings.objects.get(key='banner').value
    title = CstvSettings.objects.get(key='title').value
    context = { 'v': video, 'banner':banner, 'title':title }
    return render(request, 'cstv/play.html', context)

def getsubscribe(request, wxid):
    mylist = []
    my_list = []
    other_list = []
    for c in CstvMember.objects.filter(wxid=wxid):
        mylist.append(eval(c.channelid))
    raw = urllib2.urlopen(serverIP+"user/channelList/"+appid, timeout=5).read()
    for r in json.loads(raw)['data']:
        if r['chn_id'] in mylist:
            my_list.append(r)
        else:
            other_list.append(r)
    return HttpResponse(json.dumps({'my_list':my_list, 'other_list':other_list}))

def subscribe(request, wxid, channelid):
    try:
        CstvMember(wxid=wxid, channelid=channelid).save()
        return HttpResponse("subscribe success")
    except:
        return HttpResponse("subscribe failed")

def unsubscribe(request, wxid, channelid):
    try:
        CstvMember.objects.filter(wxid=wxid, channelid=channelid).delete()
        return HttpResponse("unsubscribe success")
    except:
        return HttpResponse("unsubscribe failed")

def redirect(request, args):
    string = ""
    for a in args.split("_"):
        string += str(a) + "/"
    try:
        return HttpResponse(urllib2.urlopen(serverIP+string, timeout=5).read().replace("\\\\n", ""))
    except:
        return HttpResponse("time out")
