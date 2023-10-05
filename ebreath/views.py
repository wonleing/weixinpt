# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.core import serializers
from django.core.serializers.json import DjangoJSONEncoder
from django.db.models.query import QuerySet
from django.utils import simplejson
from ebreath.models import *
import json, share, random, time, urllib2, random
from wxpay import build_form, xml_to_dict
appid="wx7c51dd558a1440a0" #miaochun-miniprogram
secret="833dbe493440e25350e6a0cb47a8c91e"
pay_param = {
    'appId': appid,
    'appSecret': secret,
    'mch_id': '1522108331',
    'partnerKey': 'abcd1234abcd1234abcd1234abcd1234',
    'notify_url': 'http://weixinpt.sinaapp.com/ebreath/notify'
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
    if EbreathUser.objects.filter(userid=userid, token=token):
        return False
    else:
        return True

def getsetting(request):
    stype = int(request.GET.get("type"))
    if stype > 1:
        ret = []
        for d in EbreathSetting.objects.filter(type=stype).order_by('-id'):
            ret.append({'a':d.title, 'b':d.description, 'c':d.pic, 'd':d.link.split(",")})
        return to_json(ret)
    else:
        imglist = EbreathSetting.objects.filter(type=stype).order_by('-id')
        return to_json(random.sample(imglist, 1)[0].pic)

def checkkd(request):
    oid = request.GET.get("oid")
    ret = EbreathRecord.objects.get(recordid=oid)
    return HttpResponse(urllib2.urlopen("http://123.206.26.34/html/getkdinfo.php?com="+ret.kdcom+"&nu="+ret.kdnu).read())

def memberdetail(request):
    year = 2019
    totalbalance = 0
    EbreathPay.objects.filter(amount=0).delete()
    pay = EbreathPay.objects.filter(date__year=year)
    record = EbreathRecord.objects.filter(date__year=year)
    jjjp = EbreathProduct.objects.get(productid=1)
    qgp = EbreathProduct.objects.get(productid=2)
    summary = []
    for m in range(12):
        paynum = 0
        paysum = 0
        jjj = 0
        qg = 0
        cost = 0
        for p in pay.filter(date__month=m+1):
            paynum += 1
            paysum += p.amount
        for r in record.filter(date__month=m+1):
            if r.kdcom == 'jiuye':
                jjj += r.number
                cost += r.number * jjjp.price
            else:
                qg += r.number
                cost += r.number * qgp.price
        summary.append({'paynum':paynum, 'paysum':paysum, 'jjj':jjj, 'qg':qg, 'cost':cost})
    for u in EbreathUser.objects.all():
        totalbalance += u.balance
    context = { 'year': year, 'summary': summary, 'jjjstorage': jjjp.number, 'qgstorage': qgp.number, 'totalbalance': totalbalance }
    return render(request, 'miaochun.html', context)

def userdetail(request):
    userid = int(request.GET.get("userid"))
    return to_json(EbreathUser.objects.filter(userid=userid))

def productlist(request):
    productid = request.GET.get("productid")
    onsale = request.GET.get("onsale")
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    ret = EbreathProduct.objects.all()
    if productid:
        ret = ret.filter(productid=productid)
    if onsale:
        ret = ret.filter(onsale=onsale)
    return to_json(ret[pn*pp:(pn+1)*pp])

def qalist(request):
    return to_json(EbreathQa.objects.all().order_by('id'))

def userlogin(request):
    code = request.GET.get("code")
    name = request.GET.get("name")
    pic = request.GET.get("pic")
    detail = request.GET.get("detail")
    tk = json.loads(urllib2.urlopen("https://api.weixin.qq.com/sns/jscode2session?appid="+appid+"&secret="+secret+"&js_code="+code+"&grant_type=authorization_code").read())
    try:
        ret = EbreathUser.objects.get(wxid=tk['openid'])
        return to_json({'userid':ret.userid, 'token':ret.token})
    except:
        newret = EbreathUser(wxid=tk['openid'],token=tk['session_key'],name=name,detail=detail,pic=pic)
        newret.save()
        return to_json({'userid':newret.userid, 'token':newret.token})

@csrf_exempt
def paylist(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    if params['mode'] == 'mypay':
        ret = EbreathPay.objects.filter(userid=userid)
    else:
        ret = EbreathPay.objects.filter(memberid=userid)
    return to_json(ret)

@csrf_exempt
def orderlist(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    pn = int(params['pn']) if params.has_key('pn') else 0
    pp = int(params['pp']) if params.has_key('pp') else 20
    ret = EbreathRecord.objects.filter(userid=userid).order_by('-recordid')
    if params.has_key('status'):
        ret = ret.filter(status=params['status'])
    return to_json(ret[pn*pp:(pn+1)*pp])

@csrf_exempt
def makeorder(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    productid = int(params['productid'])
    amount = int(params['amount'])
    city=params['province']
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    user = EbreathUser.objects.get(userid=userid)
    product = EbreathProduct.objects.get(productid=productid)
    total = product.price * amount
    postset = EbreathSetting.objects.get(type=4)
    if product.tag == u'限京津冀' and city != u'北京市' and city != u'天津市' and city != u'河北省':
        return HttpResponse("not sale in this area")
    if total < int(postset.title) and product.tag != u'自提专用':
        total += int(postset.description)
    if params['address'] == u'请选择配送地址':
        address = '线下自提'
    else:
        address = params['address']
    if total > user.balance or product.number < amount:
        return HttpResponse("not enough money or storage")
    else:
        try:
            EbreathRecord(userid=userid,productid=productid,number=amount,total=total,province=params['province'],city=params['city'],county=params['county'],detail=address,recname=params['username'],rectel=params['usertel'],status=1).save()
            user.balance -= total
            user.save()
            product.number -= amount
            product.save()
            return HttpResponse("order completed")
        except:
            return HttpResponse("order failed")

@csrf_exempt
def delorder(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    oid = params['oid']
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    order = EbreathRecord.objects.get(recordid=oid)
    if order.userid == userid and order.status == 1:
        user = EbreathUser.objects.get(userid=userid)
        product = EbreathProduct.objects.get(productid=order.productid)
        order.status = 2
        order.save()
        user.balance += order.total
        user.save()
        product.number += order.number
        product.save()
        return HttpResponse("order canceled")

@csrf_exempt
def payable(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    if params['memberid']:
        memberid = int(params['memberid'])
    else:
        memberid = 0
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    otid = str(userid)+'-'+str(int(time.time()))
    totalfen = float(params['amount']) * 100
    user = EbreathUser.objects.get(userid=userid)
    parameter = {
        'body': 'Guilt free yogurt',
        'openid': user.wxid,
        'out_trade_no': otid,
        'spbill_create_ip': request.META.get('REMOTE_ADDR', ''),
        'total_fee': str(int(totalfen)),
        }
    parameter.update(pay_param)
    EbreathPay(otid=otid, userid=userid, memberid=memberid).save()
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
    fee = int(total_fee)/100.0
    add = fee
    for d in EbreathSetting.objects.filter(type=2):
        if float(d.title) == fee:
            add = float(d.description)
            break
    try:
        ret = EbreathPay.objects.get(otid=otid)
        ret1 = EbreathUser.objects.get(wxid=openid)
        if ret1.userid == ret.userid:
            ret.amount = fee
            ret.save()
            if fee > 1997:
                ret1.level = 1
            ret1.total += fee
            ret1.balance += add
            ret1.save()
        if ret.memberid > 0 and ret1.userid != ret.memberid:
            rate = EbreathSetting.objects.get(type=3)
            ret2 = EbreathUser.objects.get(userid=ret.memberid)
            ret2.balance += float(rate.title) * fee
            ret2.save()
        return 'success'
    except:
        return False

@csrf_exempt
def comment(request):
    params=json.loads(request.body)
    userid = int(params['userid'])
    pid = int(params['productid'])
    content = params['content']
    if not userid or authfail(userid, params['token']):
        return HttpResponse('auth fail')
    user = EbreathUser.objects.get(userid=userid)
    if content and len(EbreathComment.objects.filter(userid=userid,productid=pid)) == 0:
        #if u'电影票友' in content and len(EbreathRecord.objects.filter(userid=userid)) == 0:
        #    user.balance += 40
        #    user.save()
        if len(EbreathRecord.objects.filter(userid=userid)) > 0:
            user.balance += 10
            user.save()
        EbreathComment(userid=userid, productid=pid, name=user.name, pic=user.pic, detail=content).save()
        return HttpResponse("comment added")
    else:
        return HttpResponse("duplicated comment")

def getcomment(request):
    pid = request.GET.get("productid")
    pn = int(request.GET.get("pn")) if request.GET.get("pn") else 0
    pp = int(request.GET.get("pp")) if request.GET.get("pp") else 20
    ret = EbreathComment.objects.filter(productid=pid, isshow=1).order_by("-id")
    return to_json(ret[pn*pp:(pn+1)*pp])
