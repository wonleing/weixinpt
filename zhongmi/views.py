# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.db.models import Q
from django.utils.encoding import smart_str
import xml.etree.ElementTree as ET
from zhongmi.models import *
import share, hashlib, random, time
TOKEN = "weixinpt"

@csrf_exempt
def handleRequest(request):
    if request.method == 'GET':
        return HttpResponse(checkSignature(request),content_type="text/plain")
    elif request.method == 'POST':
        return HttpResponse(responseMsg(request),content_type="application/xml")
    else:
        return None

def checkSignature(request):
    signature = request.GET.get("signature", None)
    timestamp = request.GET.get("timestamp", None)
    nonce = request.GET.get("nonce", None)
    echoStr = request.GET.get("echostr",None)
    tmpList = [TOKEN,timestamp,nonce]
    tmpList.sort()
    tmpstr = "%s%s%s" % tuple(tmpList)
    tmpstr = hashlib.sha1(tmpstr).hexdigest()
    if tmpstr == signature:
        return echoStr
    else:
        return None

def responseMsg(request):
    rawStr = smart_str(request.raw_post_data)
    msg = share.paraseMsgXml(ET.fromstring(rawStr))
    if msg['MsgType'] == 'event':
        if msg['Event'] == 'subscribe':
            ret = ZhongmiMain.objects.get(id=1)
            return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'mall':
                return mall(msg)
            elif msg['EventKey'] == 'howtobind':
                return share.getTextXml(msg, u'首先您需要在店铺购买商品时留下您的个人信息，然后在微信输入框中按格式输入“姓名，手机号”进行验证绑定您的个人信息，注意中间用逗号隔开。绑定成功可享受相应的商城折扣优惠')
            elif msg['EventKey'] == 'userinfo':
                return userinfo(msg)
            elif msg['EventKey'] == 'userchannel':
                return userchannel(msg)
            elif msg['EventKey'] == 'salerecord':
                return salerecord(msg)
            return share.getTextXml(msg, u'该功能尚未设定')
    elif msg['MsgType'] == 'text':
        info = msg['Content'].replace(",","，").split("，")
        if len(info) == 2 and len(info[1]) > 7:
            try:
                old = ZhongmiCustomer.objects.get(wxid=msg['FromUserName'])
                old.wxid = ""
                old.save()
            except:
                pass
            try:
                ret = ZhongmiCustomer.objects.get(name=info[0], phone=info[1])
                ret.wxid = msg['FromUserName']
                ret.save()
                return share.getTextXml(msg, u"个人信息绑定成功，您可以正常使用个人中心及折扣商城的功能了")
            except:
                return share.getTextXml(msg, u"个人信息未找到，请确认您购买时留下的个人信息已正确录入")
        elif msg['Content'] in ('mall', 'userinfo', 'userchannel', 'salerecord'):
            return eval(msg['Content'])(msg)
        else:
            try:
                ret = ZhongmiMain.objects.get(title=msg['Content'])
                if ret.type == 1:
                    return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
                elif ret.type == 3:
                    return share.getTextXml(msg, share.hongbao('zhongmi', msg['FromUserName']))
            except:
                pass
        return share.getTextXml(msg, u'您的输入不正确，更多功能请参见下方自定义菜单')

def mall(msg):
    link = ZhongmiShops.objects.get(grade=1).link
    try:
        grade = ZhongmiCustomer.objects.get(wxid=msg['FromUserName']).grade
        link = ZhongmiShops.objects.get(grade=grade).link
        return share.getTextXml(msg, u'<a href="%s">点击进入商城</a>' %link)
    except:
        return share.getTextXml(msg, u'您尚未绑定个人信息。<a href="%s">点击进入商城</a>' %link)

def userinfo(msg):
    try:
        r = ZhongmiCustomer.objects.get(wxid=msg['FromUserName'])
    except:
        return share.getTextXml(msg, u'请查看用户中心中的帮助，绑定个人信息')
    return share.getTextXml(msg, u'客户号：%s\x0a姓名：%s\x0a电话：%s\x0a性别：%s\x0a年龄：%s\x0a地址：%s \
    \x0a渠道编号：%s\x0a等级：%s\x0a推荐人电话：%s\x0a消费总额：%s\x0a积分：%s' \
    %(r.customerid, r.name, r.phone, r.gender, r.age, r.address, r.channelid, r.grade, r.saler, r.amount, r.point))

def userchannel(msg):
    try:
        r1 = ZhongmiCustomer.objects.get(wxid=msg['FromUserName'])
        r2 = ZhongmiChannel.objects.get(channelid=r1.channelid)
    except:
        return share.getTextXml(msg, u'请查看用户中心中的帮助，绑定个人信息')
    return share.getTextXml(msg, u'渠道号：%s\x0a店名：%s\x0a地址：%s\x0a电话：%s' %(r2.channelid, r2.name, r2.address, r2.phone))

def salerecord(msg):
    try:
        r1 = ZhongmiCustomer.objects.get(wxid=msg['FromUserName'])
    except:
        return share.getTextXml(msg, u'请查看用户中心中的帮助，绑定个人信息')
    message = u'最近五笔消费记录：\x0a'
    baseurl = '/zhongmi/checkdetail/'
    for r2 in ZhongmiSales.objects.filter(customerid=r1.customerid).order_by('-salesid')[:5]:
        message += u'流水号：<a href="%s?salesid=%s">%s</a>\x0a购买渠道：%s\x0a购买日期：%s\x0a总消费：%s\x0a\x0a' \
        %(baseurl, r2.salesid, r2.salesid, r2.channelid, r2.date, r2.total)
    mssage += u'更多记录请点<a href="%s?memberid=%s">这里</a>' %(baseurl, r1.customerid)
    return share.getTextXml(msg, message)

def pop(msg, number):
    try:
        ret = ZhongmiMain.objects.get(id=number)
    except:
        return share.getMultiXml(msg, '', ZhongmiMain.objects.all().order_by('id'))
    if ret.type == 0:
        return share.getTextXml(msg, ret.title+"\x0a"+"\x0a".join(ret.description.split("^")))
    elif ret.type == 1:
        return share.getSingleXml(msg, ret.title, "\x0a".join(ret.description.split("^")), ret.pic, ret.link)
    elif ret.type == 2:
        title = (ret.title, ret.description, ret.pic, ret.link)
        list = eval("Zhongmi%s" %ret.id).objects.all().order_by('id')[:9]
        return share.getMultiXml(msg, title, list)

def customerlist(request):
    word = request.POST.get('word')
    if 'login_user' in request.session and not request.session['login_user'] == "":
        customers = ZhongmiCustomer.objects.filter(channelid=request.session['login_user'])
        if word:
            customers = customers.filter(Q(name__contains=word) | Q(phone__contains=word))
    else:
        customers = ""
        request.session['login_user'] = ""
    context = { 'customers': customers,
                'login_user': request.session['login_user'] }
    return render(request, 'zhongmi/customerlist.html', context)

def customer(request):
    phone = request.GET.get('phone')
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    try:
        customer = ZhongmiCustomer.objects.get(phone=phone)
    except:
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customerlist/"></head>无此用户</html>''')
    salelist = ZhongmiCustomer.objects.filter(saler=phone)
    item = ZhongmiItems.objects.all()
    context = { 'c': customer,
                'salelist': salelist,
                'item': item,
                'login_user': request.session['login_user'] }
    return render(request, 'zhongmi/customer.html', context)

def dologin(request):
    ac = request.POST.get('account')
    pw = request.POST.get('password')
    try:
        request.session['login_user'] = ZhongmiChannel.objects.get(channelid=ac, password=pw).channelid
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customerlist/"></head>登录成功</html>''')
    except:
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customerlist/"></head>密码错误</html>''')

def updatecustomer(request):
    phone = str(request.POST.get('phone'))
    name = request.POST.get('name').replace(" ", "")
    gender = request.POST.get('gender').replace(" ", "")
    age = str(request.POST.get('age')).replace(" ", "")
    address = request.POST.get('address').replace(" ", "")
    point = str(request.POST.get('point')).replace(" ", "")
    r = ZhongmiCustomer.objects.get(phone=phone)
    r.name = name
    r.gender = gender
    r.age = age
    r.address = address
    r.point = point
    r.save()
    return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?phone=%s"></head>信息更新成功</html>''' %phone)

def inputcustomer(request):
    name = request.POST.get('name').replace(" ", "")
    phone = str(request.POST.get('phone')).replace(" ", "").replace("-", "").replace("－", "")
    gender = request.POST.get('gender').replace(" ", "")
    age = str(request.POST.get('age')).replace(" ", "")
    address = request.POST.get('address').replace(" ", "")
    saler = str(request.POST.get('saler')).replace(" ", "").replace("-", "").replace("－", "")
    channelid = request.POST.get('channelid')
    if name == "" or phone == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customerlist"></head>姓名电话不能为空</html>')
    try:
        ret = ZhongmiCustomer.objects.get(phone=phone)
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customerlist"></head>该电话已经存在</html>')
    except:
        try:
            r = ZhongmiCustomer.objects.get(phone=saler)
            r.point += 100
            r.save()
        except:
            pass
        ZhongmiCustomer(name=name, phone=phone, gender=gender, age=age, address=address, saler=saler, channelid=channelid).save()
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../customerlist"></head>会员信息添加成功</html>')

def buyitem(request):
    tprice = float(request.POST.get('total'))
    customerid = request.POST.get('customerid').replace(" ", "")
    newsale = ZhongmiSales(customerid=customerid, channelid=request.session['login_user'], total=tprice)
    newsale.save()
    for i in range(5):
        r = request.POST.get('item[%d]' %i)
        amount = request.POST.get('amount[%d]' %i)
        #return HttpResponse(itemid + " X " + amount)
        if r == "" or amount == "":
            continue
        else:
            itemid = r.split("-")[0]
            price = r.split("-")[1]
            #tprice += float(price) * int(amount)
            ZhongmiSalesdetail(salesid=newsale.salesid, itemid=int(itemid), amount=int(amount)).save()
    r1 = ZhongmiCustomer.objects.get(customerid=customerid)
    #r2 = ZhongmiShops.objects.get(grade=r1.grade)
    #dprice = tprice * r2.discount
    #newsale.total = tprice
    #newsale.save()
    r1.amount += tprice
    r1.point += tprice
    if r1.amount >= 2000 and r1.grade < 3:
        r1.grade = 3
    elif r1.amount >= 500 and r1.grade < 2:
        r1.grade = 2
    else:
        pass
    r1.save()
    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customerlist/"></head>下单成功</html>''')

def checkdetail(request):
    msg = ""
    customerid = request.GET.get('customerid')
    salesid = request.GET.get('salesid')
    if salesid:
        for i in ZhongmiSalesdetail.objects.filter(salesid=int(salesid)):
            r = ZhongmiItems.objects.get(itemid=i.itemid)
            msg += u"<p>%s，原始单价：%s，购买数量：%s</p>" %(r.name, str(r.price), str(i.amount))
        msg += u"<p><b>实际总消费：%s</b></p>" %ZhongmiSales.objects.get(salesid=salesid).total
    elif customerid:
        for r2 in ZhongmiSales.objects.filter(customerid=customerid).order_by('-salesid'):
            msg += u'<p>流水号：<a href="?salesid=%s">%s</a></p><p>购买渠道：%s</p><p>购买日期：%s\x0a</p><p>总消费：%s</p><br/>' \
            %(r2.salesid, r2.salesid, r2.channelid, r2.date, r2.total)
    if msg:
        return HttpResponse(msg)
    else:
        return HttpResponse("没有相关消费记录")

def logout(request):
    request.session['login_user'] = ""
    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customerlist/"></head>登出成功!</html>''')
