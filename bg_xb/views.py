# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.utils import simplejson
from bg_xb.models import *
import json, share, random, time, urllib2, random
from wxpay import build_form, xml_to_dict
appid="wx27415a2a31755ed6" #ilovemilk-miniprogram
secret="0b8121d8f679be85decec9aede123961"
pay_param = {
    'appId': appid,
    'appSecret': secret,
    'mch_id': '1342137701',
    'partnerKey': 'abcd1234abcd1234abcd1234abcd1234',
    'notify_url': 'http://weixinpt.sinaapp.com/bg_xb/notify'
}
def website(request, pageid):
    try:
        items = eval("BgXb%s" %pageid).objects.all().order_by('id')[:20]
    except:
        return HttpResponse(u'亲，此页不存在哦')
    return HttpResponse(serializers.serialize("json", items))

def to_json(content, indent=None):
    """return a python object as JSON API"""
    if isinstance(content, QuerySet):
        bar = serializers.get_serializer('json')()
        result = bar.serialize(content, ensure_ascii=False, indent=indent)
    else:
        result = json.dumps(content, cls=DjangoJSONEncoder, ensure_ascii=False, indent=indent)
    return HttpResponse(result, content_type='application/json', status=200) 

def authfail(userid, token):
    if BgXbUser.objects.filter(userid=userid, token=token):
        return False
    else:
        return True

def forward(request):
    aid = request.GET.get("aid")
    oid = request.GET.get("oid")
    if aid:
        ret = BgXb3.objects.get(id=aid)
        return HttpResponse(urllib2.urlopen(ret.link).read())
    elif oid:
        ret = BgXbRecord.objects.get(otid=oid)
        return HttpResponse(urllib2.urlopen("http://123.206.26.34/html/getkdinfo.php?com="+ret.kdcom+"&nu="+ret.kdnu).read())
    else:
        return HttpResponse('Unkown action')
        return HttpResponse('no article id specified')

def openimg(request):
    if request.GET.get("isbanner"):
        imglist = BgXbMain.objects.filter(type=1)
    else:
        imglist = BgXbMain.objects.filter(type=0)
    return to_json(random.sample(imglist, 1)[0].pic)

def memberdetail(request):
    memberid = request.GET.get("memberid")
    return to_json(BgXbMember.objects.filter(memberid=memberid))

def userdetail(request):
    userid = int(request.GET.get("userid"))
    return to_json(BgXbUser.objects.filter(userid=userid))

def articlelist(request):
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    return to_json(BgXb3.objects.all().order_by('id')[pn*pp:(pn+1)*pp])

def memberlist(request):
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    return to_json(BgXbMember.objects.all().order_by('-level')[pn*pp:(pn+1)*pp])

def productlist(request):
    type = request.GET.get("type")
    memberid = request.GET.get("memberid")
    productid = request.GET.get("productid")
    onsale = request.GET.get("onsale")
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    ret = BgXbProduct.objects.all().order_by('-level')
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
    return to_json(BgXbQa.objects.all().order_by('id'))

def userlogin(request):
    code = request.GET.get("code")
    name = request.GET.get("name")
    pic = request.GET.get("pic")
    detail = request.GET.get("detail")
    tk = json.loads(urllib2.urlopen("https://api.weixin.qq.com/sns/jscode2session?appid="+appid+"&secret="+secret+"&js_code="+code+"&grant_type=authorization_code").read())
    try:
        ret = BgXbUser.objects.get(wxid=tk['openid'])
        return to_json({'userid':ret.userid, 'token':ret.token})
    except:
        newret = BgXbUser(wxid=tk['openid'],token=tk['session_key'],name=name,detail=detail,pic=pic)
        newret.save()
        return to_json({'userid':newret.userid, 'token':newret.token})

@csrf_exempt
def colmember(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    memberid = params["memberid"]
    action = params["action"]
    if action == 'add':
        try:
            BgXbColmember.objects.get(user__userid=userid, member__memberid=memberid)
            return HttpResponse('nothing to add')
        except:
            u = BgXbUser.objects.get(userid=userid)
            m = BgXbMember.objects.get(memberid=memberid)
            BgXbColmember(user=u, member=m).save()
    elif action == 'del':
        try:
            BgXbColmember.objects.get(user__userid=userid, member__memberid=memberid).delete()
        except:
            return HttpResponse('nothing to delete')
    elif action == 'query':
        try:
            BgXbColmember.objects.get(user__userid=userid, member__memberid=memberid)
            return HttpResponse('True')
        except:
            return HttpResponse('False')
    return HttpResponse('%s done' %action)

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
            BgXbColproduct.objects.get(user__userid=userid, product__productid=productid)
            return HttpResponse('nothing to add')
        except:
            u = BgXbUser.objects.get(userid=userid)
            p = BgXbProduct.objects.get(productid=productid)
            BgXbColproduct(user=u, product=p).save()
    elif action == 'del':
        try:
            BgXbColproduct.objects.get(user__userid=userid, product__productid=productid).delete()
        except:
            return HttpResponse('nothing to delete')
    elif action == 'query':
        try:
            BgXbColproduct.objects.get(user__userid=userid, product__productid=productid)
            return HttpResponse('True')
        except:
            return HttpResponse('False')
    return HttpResponse('%s done' %action)

@csrf_exempt
def colmemberlist(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    pn = int(params['pn']) if params.has_key('pn') else 0
    pp = int(params['pp']) if params.has_key('pp') else 20
    ret = []
    for r in BgXbColmember.objects.filter(user__userid=userid)[pn*pp:(pn+1)*pp]:
        ret.append({'memberid':r.member.memberid, 'name':r.member.name, 'level':r.member.level, 'pic':r.member.pic, 'detail':r.member.detail})
    return to_json(ret)

@csrf_exempt
def colproductlist(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    pn = int(params['pn']) if params.has_key('pn') else 0
    pp = int(params['pp']) if params.has_key('pp') else 20
    ret = []
    for r in BgXbColproduct.objects.filter(user__userid=userid)[pn*pp:(pn+1)*pp]:
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
    ret = BgXbRecord.objects.filter(userid=userid)
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
    order = BgXbRecord.objects.get(otid=oid)
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
    user = BgXbUser.objects.get(userid=userid)
    if address:
        user.address = address
        user.save()
    for od in orders:
        pid = int(od['productid'])
        nb = int(od['number'])
        item = BgXbProduct.objects.get(productid=pid)
        total = item.price * nb
        BgXbRecord(otid=otid,userid=userid,productid=pid,number=nb,detail=params['goodname']+":"+user.address,total=total,status=2).save()
        totalfen += int(total * 100)
    parameter = {
        'body': 'ilovemilk wxpay',
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
        ret = BgXbUser.objects.get(wxid=openid)
        ret.total += int(total_fee)/100.0
        ret.save()
    except:
        return False
    for rc in BgXbRecord.objects.filter(otid=otid):
        rc.status = 1
        rc.save()
    return 'success'
