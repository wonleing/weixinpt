# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.utils import simplejson
from xgxm.models import *
import json, share, random, time, urllib2, random
from wxpay import build_form, xml_to_dict
appid="wx55571401979f5b4b" #cheesecurd-miniprogram
secret="fe6bfdad8b6a5bbfb0e1566b40fc1aae"
pay_param = {
    'appId': appid,
    'appSecret': secret,
    'mch_id': '1501855171',
    'partnerKey': 'abcd1234abcd1234abcd1234abcd1234',
    'notify_url': 'http://weixinpt.sinaapp.com/xgxm/notify'
}

def to_json(content, indent=None):
    """return a python object as JSON API"""
    if isinstance(content, QuerySet):
        bar = serializers.get_serializer('json')()
        result = bar.serialize(content, ensure_ascii=False, indent=indent)
    else:
        result = json.dumps(content, cls=DjangoJSONEncoder, ensure_ascii=False, indent=indent)
    return HttpResponse(result, content_type='application/json', status=200) 

def authfail(userid, token):
    if XgxmUser.objects.filter(userid=userid, token=token):
        return False
    else:
        return True

def forward(request):
    aid = request.GET.get("aid")
    oid = request.GET.get("oid")
    if aid:
        ret = XgxmMain.objects.get(id=aid)
        return HttpResponse(urllib2.urlopen(ret.link).read())
    elif oid:
        ret = XgxmRecord.objects.get(otid=oid)
        return HttpResponse(urllib2.urlopen("http://123.206.26.34/html/getkdinfo.php?com="+ret.kdcom+"&nu="+ret.kdnu).read())
    else:
        return HttpResponse('Unkown action')

def openimg(request):
    if request.GET.get("isbanner"):
        imglist = XgxmMain.objects.filter(type=1)
    else:
        imglist = XgxmMain.objects.filter(type=0)
    return to_json(random.sample(imglist, 1)[0].pic)

def memberdetail(request):
    memberid = request.GET.get("memberid")
    return to_json(XgxmMember.objects.filter(memberid=memberid))

def userdetail(request):
    userid = int(request.GET.get("userid"))
    return to_json(XgxmUser.objects.filter(userid=userid))

def articlelist(request):
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    return to_json(XgxmMain.objects.filter(type=2).order_by('id')[pn*pp:(pn+1)*pp])

def memberlist(request):
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    return to_json(XgxmMember.objects.all().order_by('-level')[pn*pp:(pn+1)*pp])

def productlist(request):
    type = request.GET.get("type")
    memberid = request.GET.get("memberid")
    productid = request.GET.get("productid")
    onsale = request.GET.get("onsale")
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    ret = XgxmProduct.objects.all().order_by('-level')
    if productid:
        ret = ret.filter(productid=productid)
    if memberid:
        ret = ret.filter(member__memberid=memberid)
    if type:
        ret = ret.filter(type=type)
    if onsale:
        ret = ret.filter(onsale=onsale)
    return to_json(ret[pn*pp:(pn+1)*pp])

def qalist(request):
    return to_json(XgxmQa.objects.all().order_by('id'))

def userlogin(request):
    code = request.GET.get("code")
    name = request.GET.get("name")
    pic = request.GET.get("pic")
    detail = request.GET.get("detail")
    tk = json.loads(urllib2.urlopen("https://api.weixin.qq.com/sns/jscode2session?appid="+appid+"&secret="+secret+"&js_code="+code+"&grant_type=authorization_code").read())
    try:
        ret = XgxmUser.objects.get(wxid=tk['openid'])
        return to_json({'userid':ret.userid, 'token':ret.token})
    except:
        newret = XgxmUser(wxid=tk['openid'],token=tk['session_key'],name=name,detail=detail,pic=pic)
        newret.save()
        return to_json({'userid':newret.userid, 'token':newret.token})

@csrf_exempt
def colproduct(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    productid = params["productid"]
    action = params["action"]
    if action == 'add':
        try:
            XgxmColproduct.objects.get(user__userid=userid, product__productid=productid)
            return HttpResponse('nothing to add')
        except:
            u = XgxmUser.objects.get(userid=userid)
            p = XgxmProduct.objects.get(productid=productid)
            XgxmColproduct(user=u, product=p).save()
    elif action == 'del':
        try:
            XgxmColproduct.objects.get(user__userid=userid, product__productid=productid).delete()
        except:
            return HttpResponse('nothing to delete')
    elif action == 'query':
        try:
            XgxmColproduct.objects.get(user__userid=userid, product__productid=productid)
            return HttpResponse('True')
        except:
            return HttpResponse('False')
    return HttpResponse('%s done' %action)

@csrf_exempt
def colproductlist(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    pn = int(params['pn']) if params.has_key('pn') else 0
    pp = int(params['pp']) if params.has_key('pp') else 20
    ret = []
    for r in XgxmColproduct.objects.filter(user__userid=userid)[pn*pp:(pn+1)*pp]:
        ret.append({'productid':r.product.productid, 'title':r.product.title, 'level':r.product.level, 'pic':r.product.pic, 'type':r.product.type, 'price':r.product.price, 'tag':r.product.tag, 'onsale':r.product.onsale})
    return to_json(ret)

@csrf_exempt
def orderlist(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    pn = int(params['pn']) if params.has_key('pn') else 0
    pp = int(params['pp']) if params.has_key('pp') else 20
    ret = XgxmRecord.objects.filter(userid=userid)
    if params.has_key('status'):
        ret = ret.filter(status=params['status'])
    return to_json(ret[pn*pp:(pn+1)*pp])

@csrf_exempt
def delorder(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    oid = params['oid']
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    order = XgxmRecord.objects.get(otid=oid)
    if order.userid == userid and order.status == 2:
        order.delete()
        return HttpResponse("unpaied order deleted")

@csrf_exempt
def payable(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    address = params['address']
    orders = params['orders']
    otid = str(userid)+'-'+str(int(time.time()))
    totalfen = 0
    user = XgxmUser.objects.get(userid=userid)
    if address:
        user.address = address
        user.save()
    for od in orders:
        pid = int(od['productid'])
        nb = int(od['number'])
        item = XgxmProduct.objects.get(productid=pid)
        total = item.price * nb
        XgxmRecord(otid=otid, userid=userid, productid=pid, number=nb, detail=params['goodname']+":"+user.address, total=total, status=2).save()
        totalfen += int(total * 100)
    parameter = {
        'body': 'cheesecurd wxpay',
        'openid': user.wxid,
        'out_trade_no': otid,
        'spbill_create_ip': request.META.get('REMOTE_ADDR', ''),
        'total_fee': str(totalfen),
        }
    parameter.update(pay_param)
    return to_json(build_form(parameter))

@csrf_exempt
def notify(request):
    params = xml_to_dict(request.body)
    otid = params['out_trade_no']
    openid = params['openid']
    total_fee = params['total_fee']
    if params['return_code'] == 'SUCCESS':
        if checkin(openid, otid, total_fee) == 'success':
            return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
    return HttpResponse('WX Notify not recognized!')

def checkin(openid, otid, total_fee):
    try:
        ret = XgxmUser.objects.get(wxid=openid)
        ret.total += int(total_fee)/100.0
        ret.save()
    except:
        return False
    for rc in XgxmRecord.objects.filter(otid=otid):
        rc.status = 1
        rc.save()
    return 'success'
