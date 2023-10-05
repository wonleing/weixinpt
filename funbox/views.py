# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.encoding import smart_str
from django.db.models import Q
from django.core import serializers
import xml.etree.ElementTree as ET
from funbox.models import *
import share, hashlib, time, datetime, random, urllib2, json, string, re
from wxpay import build_form, xml_to_dict
import alipay
TOKEN = "weixinpt"
jylogo = "http://ww1.sinaimg.cn/mw690/558fe6e3gw1ejyiw14pomj20960640su.jpg"
welcome = u'''欢迎来到捷优电子支付系统，商户请点击商家功能，消费者请点击消费查询'''
readme = u'''请点击菜单中商户中心进行收款渠道注册，成功后会绑定当前微信号为收款管理员，随后方可收到收款提醒、使用快速查帐及商户中心功能。'''
appid="wx99dc9d6300c74126" #jyousoft
secret="bf2613e13e8f4ead30f6e89248e3c769"
template="Ts4enYtd8Qbmtq8LNRkmaVMPhs0W-kVkwUz_oeqDsd0"
access_url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s"
remind_url = "https://api.weixin.qq.com/cgi-bin/message/template/send?access_token=%s"
pay_param = {
    'appId': appid,
    'appSecret': secret,
    'mch_id': '1309378601',
    'partnerKey': '1234qwerasdfzxcv1234qwerasdfzxcv',
    'notify_url': 'http://weixinpt.sinaapp.com/funbox/payment_notify_wx/'
}
aliappid = "2016012101111751"
ali_notify_url = "http://weixinpt.sinaapp.com/funbox/payment_notify_ali/"
return_url = 'http://weixinpt.sinaapp.com/funbox/comment?rawid=ali&memberid=%s'
aligateway = 'https://openapi.alipay.com/gateway.do?'
app_private_key_string ='''-----BEGIN RSA PRIVATE KEY-----
MIICXAIBAAKBgQCqYWz4wRDvi8bPnGmGB1+kg5wBEXotz9FE66utkN9Z5xol2BpGunva5x9mjupQ4kE4LHT2KsdwE5VloVlfhgCCuJ+fEPn31LsBlXUtk1eIfOfK1xz4PSgrYhKw+41otHpXfMcl4Jnf8hZ1wZvmI+L6UZF29fatF9xIz94aWbbirwIDAQABAoGAJIzP3rE0G99FYAYy0PDGALnG/qesKSW6w+k2o/4/G78q6dFpGaEprrUEFHE2LPHMgetvj9tve0iINQwe6xIJC6g+WaIrDyALbJmphF7bQ7Cf7Bue5h/iJvEHtyBXdkKI12IPK25OcMWr5H0ef0uIc4PMh4IL1fgndgBWvKk8+fkCQQDXwSHKb/qVKTTqumqbElivz+Db6NLdV4rIA/k5P3BW7qhaSORap6rPx/EYaVEA0wsYa6cw4ZAzvXgQ/xOhjVsVAkEAyimRNHaOD/q+iQEe2HKXB6RwAfWHq5h+BQX02V1Yhu7MDWpTj0V+daMYkn3CiAkfmZTmI2FofrTtaQCfLwAnswJAXW7g0EcQEFpo9SHHmuImD/UJHpLEBmCr1BSMcDM91hfCRl78rRmhChw/F2A8WQwL6QZtv+hex1lMzqd3++U4RQJBAJaW1BUSYsxAaYHAleuBoEMPGGg9LyyBUQ4I29S2leUdKF6t30SP7Z1POlSU3T1cHm/W3H9qZd5Mg7R9xBXMtcUCQGYc+uqzG8dG9yT8DQzuTxxnLUjG+PpM8PmwxEC3vCigk0JiqtSZ4BVNnPO6awNsvjgeIsdfYWaJk3ccSoV6mpk=
-----END RSA PRIVATE KEY-----'''
alipay_public_key_string = '''-----BEGIN PUBLIC KEY-----
MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQKBgQDDI6d306Q8fIfCOaTXyiUeJHkrIvYISRcc73s3vF1ZT7XN8RNPwJxo8pWaJMmvyTn9N4HQ632qJBVHf8sxHi/fEsraprwCtzvzQETrNRwVxLO5jVmRGi60j8Ue1efIlzPXV9je9mkjzOmdssymZkh2QhUrCmZYI/FCEa3/cNMW0QIDAQAB
-----END PUBLIC KEY-----'''

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
            return share.getTextXml(msg, welcome)
        elif msg['Event'] == 'CLICK':
            if msg['EventKey'] == 'readme':
                return share.getTextXml(msg, readme)
            elif msg['EventKey'] == 'shoplist':
                return shoplist(msg)
            elif msg['EventKey'] == 'qcheck':
                return qcheck(msg)
            elif msg['EventKey'] == 'scheck':
                return scheck(msg)
            elif msg['EventKey'] == 'ucheck':
                return ucheck(msg)
            else:
                return share.getTextXml(msg, u'该功能尚未设定')
    elif msg['MsgType'] == 'text':
        return share.getTextXml(msg, welcome)

def shoplist(msg):
    return share.getSingleXml(msg, "点击查看入驻商家", "", jylogo, "http://weixinpt.sinaapp.com/funbox/index/?wxid="+msg['FromUserName'])

def qcheck(msg):
    ret = FunboxMember.objects.filter(wxid=msg['FromUserName'])
    if len(ret) == 1:
        return share.getTextXml(msg, u'您当前余额是：%s\x0a累计总收为%s\x0a查看详情与申请提现请进入商户中心' %(ret[0].balance, ret[0].total))
    elif len(ret) > 1:
        return share.getTextXml(msg, 'wxid duplicated')
    else:
        return share.getSingleXml(msg, "您尚未注册为商户，请点击进行注册", "", jylogo, "http://weixinpt.sinaapp.com/funbox/bind/?wxid="+msg['FromUserName'])

def scheck(msg):
    ret = FunboxMember.objects.filter(wxid=msg['FromUserName'])
    if len(ret) == 1:
        return share.getSingleXml(msg, "点击进入商户中心", "", jylogo, "http://weixinpt.sinaapp.com/funbox/checkdetail/?wxid="+msg['FromUserName'])
    elif len(ret) > 1:
        return share.getTextXml(msg, 'wxid duplicated')
    else:
        return share.getSingleXml(msg, "点击进行商户注册", "", jylogo, "http://weixinpt.sinaapp.com/funbox/bind/?wxid="+msg['FromUserName'])

def ucheck(msg):
    ret = FunboxUser.objects.filter(wxid=msg['FromUserName'])
    if len(ret) == 1:
        return share.getSingleXml(msg, "点击查看消费信息", "", jylogo, "http://weixinpt.sinaapp.com/funbox/userdetail/?wxid="+msg['FromUserName'])
    elif len(ret) > 1:
        return share.getTextXml(msg, 'wxid duplicated')
    else:
        user = FunboxUser(wxid=msg['FromUserName'], type=0, jointime=str(datetime.date.today()))
        user.save()
        return share.getSingleXml(msg, "新用户，点击编辑信息", "", jylogo, "http://weixinpt.sinaapp.com/funbox/userdetail/?wxid="+user.wxid)

def index(request):
    t = request.GET.get('type')
    perpage = request.GET.get('perpage')
    pageno = request.GET.get('pageno')
    request.session['openid'] = request.GET.get('wxid')
    if not t or t == 'all':
        ret = FunboxMember.objects.filter(type__gt=0)
    else:
        ret = FunboxMember.objects.filter(type=int(t))
    if perpage and pageno:
        ret = ret[int(perpage)*int(pageno)-int(perpage):int(perpage)*int(pageno)]
    baseurl = 'http://weixinpt.sinaapp.com/funbox/chargepage/?memberid='
    if request.GET.get('json'):
        context = { 'memberlist':serializers.serialize("json", ret), 'baseurl':baseurl }
        return HttpResponse(str(context))
    else:
        context = { 'memberlist':ret, 'baseurl':baseurl }
        return render(request, 'funbox/index.html', context)

def chargepage(request):
    memberid = request.GET.get('memberid')
    if 'openid' in request.session:
        openid = request.session['openid'] #读取缓存
        try:
            payer = FunboxUser.objects.get(wxid=openid)
        except:
            payer = FunboxUser(wxid=openid, type=0, jointime=str(datetime.date.today()))
            payer.save()
        balance = payer.balance
    else:
        openid = ''
        balance = 0
    ret = FunboxMember.objects.filter(memberid=memberid)
    if len(ret) != 1:
        return HttpResponse('未找到该加盟商')
    comments = []
    cmt = FunboxComment.objects.filter(memberid=memberid)
    cm0 = len(cmt.filter(status=0))
    cm1 = len(cmt.filter(status=1))
    cm2 = len(cmt.filter(status=2))
    cm3 = len(cmt.filter(status=3))
    cm4 = len(cmt.filter(status=4))
    cm5 = len(cmt.filter(status=5))
    cnumber = len(cmt)
    if cnumber > 0:
        crate = str((cm1+(cm2*2)+(cm3*3)+(cm4*4)+(cm5*5))/float(cnumber))[:4]
    else:
        crate = 0
    for c in cmt.order_by('-commentid')[:20]:
        user = FunboxUser.objects.get(userid=c.userid)
        dname = user.name or user.phone or '匿名'
        image = user.pic if user.pic else "http://ww3.sinaimg.cn/mw690/558fe6e3gw1f10cjzp6u3j208c08cq38.jpg"
        comments.append({'dname':dname, 'status':c.status, 'tip':c.tip, 'image':image, 'content':c.content, 'date':c.date})
    if request.GET.get('json'):
        context = { 'minfo':serializers.serialize("json", ret), 'openid':openid, 'balance':balance, 'comments':str(comments),
        'cnumber':cnumber, 'crate':crate }
        return HttpResponse(str(context))
    else:
        context = { 'minfo':ret[0], 'openid':openid, 'balance':balance, 'comments':comments, 'cnumber':cnumber, 'crate':crate }
        return render(request, 'funbox/chargepage.html', context)

def bind(request):
    openid = request.GET.get('wxid')
    context = { 'openid':openid }
    return render(request, 'funbox/bind.html', context)

@csrf_exempt
def dobind(request):
    openid = request.POST.get('openid')
    memberid = request.POST.get('memberid')
    password = request.POST.get('password')
    type = request.POST.get('type')
    account = request.POST.get('account')
    fromagent = request.POST.get('fromagent')
    if not (memberid and password):
        return HttpResponse('渠道代号、密码、商户类型、帐户都必须填写')
    else:
        try:
            ret = FunboxMember.objects.get(memberid=memberid)
            if ret.password == password:
                ret.wxid = openid
                ret.save()
                return HttpResponse('渠道所绑定微信已更新，商户类型与提现帐户未更改。请返回并点击菜单进入商户中心')
            else:
                return HttpResponse('渠道已存在，但输入密码不正确')
        except:
            if not (type and account):
                return HttpResponse('商户类型、帐户都必须填写')
            FunboxMember(wxid=openid, memberid=memberid, type=type, account=account, password=password).save()
            return HttpResponse("收款渠道注册绑定成功，请返回并点击菜单进入商户中心进行详细内容设置并生成收款二维码")

def checkdetail(request):
    ret1 = FunboxMember.objects.get(wxid=request.GET.get('wxid'))
    memberid = ret1.memberid
    ret2 = FunboxRecord.objects.filter(memberid=memberid).order_by("-date")
    ret3 = FunboxMsg.objects.filter(memberid=memberid).order_by("-date")
    if request.GET.get('json'):
        context = { 'minfo':serializers.serialize("json", ret1), 'inlist':serializers.serialize("json", ret2), 'outlist':serializers.serialize("json", ret3)}
        return HttpResponse(str(context))
    else:
        context = { 'minfo': ret1, 'inlist': ret2, 'outlist': ret3 }
        return render(request, 'funbox/checkdetail.html', context)

def userdetail(request):
    ret1 = FunboxUser.objects.filter(wxid=request.GET.get('wxid'))
    userid = ret1[0].userid
    ret2 = FunboxRecord.objects.filter(userid=userid).order_by("-date")
    if request.GET.get('json'):
        context = { 'userinfo':serializers.serialize("json", ret1), 'spendlist':serializers.serialize("json", ret2) }
        return HttpResponse(str(context))
    else:
        context = { 'userinfo': ret1[0], 'spendlist': ret2 }
        return render(request, 'funbox/userdetail.html', context)

def qrcode(request):
    baseurl = 'https://api.nbhao.org/v1/qrcode/make?text=http://weixinpt.sinaapp.com/funbox/chargepage/?memberid='
    memberid = request.GET.get('memberid')
    try:
        ret = FunboxMember.objects.get(memberid=memberid)
    except:
        return HttpResponse('<h1>无此商户</h1>')
    context = { 'baseurl':baseurl, 'minfo': ret }
    return render(request, 'funbox/qrcode.html', context)

def doin(c):
    if c['paid'] and c['livemode']:
        if FunboxRecord.objects.filter(orderid=c['id']):
            return ('Order already processed')
        if c['body'] == "Your Body":
            c['body'] = "1-0.1"
            c['subject'] = 'wonleing'
        sbody = c['body'].split('-')
        income = c['amount']/100.0 + float(sbody[1])
        try:#商户入帐
            ret = FunboxMember.objects.get(memberid=c['subject'])
        except:
            return HttpResponse('Member %s not found' %c['subject'])
        if ret.man == 0:
            if ret.jian != 0 and income >= ret.jian:
                m_return = int(random.random()*200)/100.0
            else:
                m_return = 0
        else:
            m_return = int(income/ret.man)*ret.jian
        m_realin = income-m_return
        ret.balance += m_realin
        ret.total += m_realin
        ret.save()
        #商户提醒
        body={"touser":ret.wxid,
              "template_id":template,
              "url":"",
              "topcolor":"#173177",
              "data":{
              "keyword1":{"value":str(datetime.datetime.now())[:-7],"color":"#173177"},
              "keyword2":{"value":c['channel'],"color":"#173177"},
              "keyword3":{"value":str(m_realin),"color":"#173177"},
              "keyword4":{"value":c['subject'],"color":"#173177"},
              "keyword5":{"value":c['id'],"color":"#173177"}}}
        token = json.loads(urllib2.urlopen(access_url%(appid,secret)).read())['access_token']
        urllib2.urlopen(urllib2.Request(remind_url%token, json.dumps(body, ensure_ascii=False)))
        try:#消费者入帐
            ret1 = FunboxUser.objects.get(userid=int(sbody[0]))
            ret1.total += c['amount']/100.0
            ret1.balance += m_return - float(sbody[1])
            ret1.save()
        except:
            ret1 = FunboxUser(wxid=openid, type=1, jointime=str(datetime.date.today())) #新建支付宝用户
            ret1.total += income
            ret1.balance += m_return - pb
            ret1.save()
        detail = u"商家实收"+str(m_realin)+u"返现"+str(m_return)+u"（"+sbody[1]+u"来自余额）"
        FunboxRecord(orderid=c['id'], memberid=c['subject'], userid=int(sbody[0]), type=c['channel'], detail=detail, \
        amount=m_realin, status=1).save()
        return HttpResponse('Order %s Created' %c['id'])

def updatein(c):
    if c['object']=='refund' and c['status']=='succeeded':
        refund = c['amount']/100.0
        orderid = c['charge']
        try:
            ret = FunboxRecord.objects.get(orderid=orderid)
        except:
            return HttpResponseNotFound("Error: Order %s not found" %orderid)
        ret2 = FunboxMember.objects.get(memberid=ret.memberid)
        ret2.balance -= refund
        ret2.total -= refund
        ret2.save(update_fields=['balance', 'total'])
        ret.status = 0
        ret.detail = c["description"] + u"。已退款：" + str(refund)
        ret.save(update_fields=['status', 'detail'])
        return HttpResponse('Order %s Updated' %orderid)

@csrf_exempt
def doout(request):
    memberid = request.POST.get('memberid')
    amount = float(request.POST.get('amount'))
    try:
        ret = FunboxMember.objects.get(memberid=memberid)
    except:
        return HttpResponse('未找到该加盟商')
    if amount > ret.balance:
        return HttpResponse('余额不足，不能完成指定金额的提现')
    elif amount <= 500:
        return HttpResponse('提现金额必须大于500元')
    else:
        FunboxMsg(memberid=memberid, amount=amount, accountinfo=ret.accountinfo, status=0).save()
        ret.balance -= amount
        ret.save()
        return HttpResponse('提现申请完成，预计1－2个工作日到账')

def comment(request):
    memberid = request.GET.get('memberid')
    rawid = request.GET.get('rawid')
    try:
        rawid = FunboxUser.objects.get(wxid=rawid).userid
    except:
        rawid = ''
    try:
        FunboxMember.objects.get(memberid=memberid)
    except:
        return HttpResponse('<h1>未找到该加盟商</h1>')
    context = { 'memberid': memberid, 'userid': rawid }
    return render(request, 'funbox/comment.html', context)

@csrf_exempt
def docomment(request):
    userid = request.POST.get('userid')
    phone = request.POST.get('phone')
    memberid = request.POST.get('memberid')
    content = request.POST.get('content')
    status = request.POST.get('status')
    if not userid and not phone:
        return HttpResponse('<h1>请填写电话</h1>')
    elif phone:
        try:
            user = FunboxUser.objects.get(phone=phone)
        except:
            user = FunboxUser(type=1, phone=phone, jointime=str(datetime.date.today()))
            user.save()
    else:
        user = FunboxUser.objects.get(userid=userid)
    userid = user.userid
    #if not FunboxComment.objects.filter(Q(memberid=memberid) | Q(userid=user.userid)) and user.total<10:
    #    user.balance += 1
    #    user.total += 1
    #    user.save()
    if not status:
        status = 5 
    try:
        highpoints = re.compile(u'[\U00010000-\U0010ffff]')
    except re.error:
        highpoints = re.compile(u'[\uD800-\uDBFF][\uDC00-\uDFFF]')
    content = highpoints.sub(u'\u25FD', content)
    FunboxComment(memberid=memberid, userid=int(userid), content=content, status=int(status)).save()
    return HttpResponse('<img src="http://ww1.sinaimg.cn/mw690/558fe6e3gw1f10ck11mg7j20ku0zkdjj.jpg" width="100%"/>')

@csrf_exempt
def pingserver(request):
    import os,sys
    path_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0,path_dir)
    import pingpp
    params = json.loads(request.body)
    if params['uid'].isdigit(): #Non-Wechat, params['uid'] is userid
        userid = int(params['uid'])
    elif params['uid']: #Wechat user, but still may use Alipay. params['uid'] is openid
        try:
            userid = FunboxUser.objects.get(wxid=params['uid']).userid
        except:
            newuser = FunboxUser(wxid=params['uid'], type=0, phone='', jointime=str(datetime.date.today()))
            newuser.save()
            userid = newuser.userid
    orderno = ''.join(random.sample(string.ascii_letters + string.digits, 8))
    if params['channel'] == 'alipay_wap':
        extra = dict(
            success_url='http://weixinpt.sinaapp.com/funbox/comment/?memberid='+params['order_no']+'%26rawid='+str(params['uid']),
            cancel_url='http://weixinpt.sinaapp.com/funbox/index/'
        )
    elif params['channel'] == 'wx_pub':
        extra = dict(
            open_id=params['open_id']
        )
        del params['open_id']
    else:
        extra = {}
    if isinstance(params, dict):
        params['app'] = dict(id="app_OOW14CavjnX9Syrv")
        params['currency'] = 'cny'
        params['client_ip'] = '127.0.0.1'
        params['subject'] = params['order_no']
        params['body'] = str(userid) + "-" + str(params['balance_change'])
        params['order_no'] = orderno
        params['extra'] = extra
        del params['uid']
        del params['balance_change']
    response_charge = pingpp.Charge.create(api_key=pingpp.api_key, **params)
    return HttpResponse(json.dumps(response_charge), mimetype='application/json,charset=UTF-8')

@csrf_exempt
def webhooks(request):
    params = json.loads(request.body)
    if params['type'] == 'charge.succeeded':
        doin(params['data']['object'])
    elif params['type'] == 'refund.succeeded':
        updatein(params['data']['object'])
    return HttpResponse(params['type'])

@csrf_exempt
def dologin(request):
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    memberid = request.POST.get('memberid')
    isb = request.POST.get('isb')
    if isb=='0':
        try:
            ret = FunboxUser.objects.get(phone=phone, password=password)
            return HttpResponse(ret.userid)
        except:
            return HttpResponse("登录失败")
    else:
        try:
            ret = FunboxMember.objects.get(memberid=memberid, password=password)
            return HttpResponse(ret.memberid)
        except:
            return HttpResponse("登录失败")

###NOT USED###
def register(request):
    inputid = request.GET.get('memberid')
    password = request.GET.get('password')
    code = request.GET.get('code')
    if inputid:
        ret1 = FunboxMember.objects.filter(memberid=inputid, password=password, type=0)
    else:
        tk = json.loads(urllib2.urlopen("https://api.weixin.qq.com/sns/oauth2/access_token?appid="+appid+"&secret="+secret+"&code="+code+"&grant_type=authorization_code").read())
        if 'openid' in tk:
            openid = tk['openid'] #重新生成
        elif 'openid' in request.session:
            openid = request.session['openid'] #缓存
        else:
            openid = ''
        ret1 = FunboxMember.objects.filter(wxid=openid, type=0)
    if len(ret1) != 1:
        return HttpResponse('<h1>只有代理商才可以注册商户</h1>')
    else:
        agent = ret1[0].memberid
        request.session['openid'] = openid
        context = { 'agent':agent }
        return render(request, 'funbox/register.html', context)

###NOT USED###
@csrf_exempt
def doregister(request):
    isb = request.POST.get('isb')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    type = request.POST.get('type')
    name = request.POST.get('name')
    pic = request.POST.get('pic')
    description = request.POST.get('description')
    memberid = request.POST.get('memberid')
    accountinfo = request.POST.get('accountinfo')
    agent = request.POST.get('agent')
    man = request.POST.get('man')
    jian = request.POST.get('jian')
    if isb=='0':
        if not (phone and password and type):
            return HttpResponse('电话、密码不能为空')
        try:
            ret = FunboxMember.objects.get(phone=phone)
            ret.password = password
            ret.name = name
            ret.type = type
            ret.pic = pic
            ret.description = description
        except:
            ret = FunboxUser(phone=phone, password=password, name=name, type=type, pic=pic, description=description, \
            jointime=str(datetime.date.today()))
        ret.save()
        return HttpResponse(ret.userid)
    else:
        if not (memberid and password and type and name and accountinfo):
            return HttpResponse('所有项目均须填写')
        if FunboxMember.objects.filter(memberid=memberid):
            return HttpResponse('此商户ID已注册过')
        else:
            newmember = FunboxMember(memberid=memberid, password=password, name=name, type=type, description=description, \
            man=man, jian=jian, accountinfo=accountinfo, fromagent=agent, jointime=str(datetime.date.today()))
            newmember.save()
            return HttpResponse(newmember.memberid + u'注册成功')

@csrf_exempt
def updateuser(request):
    userid = request.POST.get('userid')
    memberid = request.POST.get('memberid')
    phone = request.POST.get('phone')
    password = request.POST.get('password')
    name = request.POST.get('name')
    pic = request.POST.get('pic')
    logo = request.POST.get('logo')
    description = request.POST.get('description')
    address = request.POST.get('address')
    if userid:
        ret = FunboxUser.objects.filter(userid=userid)[0]
    elif memberid:
        ret = FunboxMember.objects.filter(memberid=memberid)[0]
    else:
        return HttpResponse('无法找到修改对象')
    try:
        ret.password = password
        ret.name = name
        ret.pic = pic
        ret.description = description
        ret.address =  address
        ret.phone = phone
        ret.logo = logo
        ret.save()
        return HttpResponse('信息更新成功')
    except:
        return HttpResponse('更新失败，请重新再试')

@csrf_exempt
def uploadimg(request):
    type = request.GET.get('type')
    ext = request.GET.get('ext')
    url = 'http://123.206.26.34/html/upload/upload.php?type='+type+'&ext='+ext
    request = urllib2.Request(url, request.body)
    response = urllib2.urlopen(request)
    return HttpResponse(response.read())

def tip(request):
    inputid = request.GET.get('memberid')
    password = request.GET.get('password')
    if inputid and password:
        ret1 = FunboxMember.objects.filter(memberid=inputid, password=password, type=0)
    elif 'openid' not in request.session:
        return HttpResponse('<h1>请重新登录商户户中心</h1>')
    else:
        ret1 = FunboxMember.objects.filter(wxid=request.session['openid'])
    if len(ret1) != 1:
        return HttpResponse('<h1>商户认证失败</h1>')
    else:
        comments = []
        for c in FunboxComment.objects.filter(memberid=ret1[0].memberid, tip=0).order_by('-commentid'):
            u = FunboxUser.objects.get(userid=c.userid)
            comments.append({'pic':u.pic, 'name':u.name or u.phone or u'匿名', 'commentid':c.commentid, 'status':c.status,
            'content':c.content, 'date':c.date})
        context = { 'comments':comments }
        return render(request, 'funbox/tip.html', context)

@csrf_exempt
def dotip(request):
    commentid = request.POST.get('commentid')
    tipamount = 1
    ret = FunboxComment.objects.get(commentid=int(commentid))
    if ret.tip > 0:
        return HttpResponse('该评论已打赏过')
    else:
        ret1 = FunboxMember.objects.get(memberid=ret.memberid)
        if ret1.balance < tipamount:
            return HttpResponse('商户余额需大于%d元' %tipamount)
        else:
            ret.tip += tipamount
            ret.save()
            ret1.balance -= tipamount
            ret1.save()
            ret2 = FunboxUser.objects.get(userid=ret.userid)
            ret2.balance += tipamount
            ret2.save()
            return HttpResponse('成功打赏%d元' %tipamount)

@csrf_exempt
def payment_notify_ali(request):
    otid = request.POST.get('out_trade_no')
    transaction_id = request.POST.get('trade_no')
    userid = request.POST.get('buyer_id')
    bank_type = 'alipay'
    if (request.POST.get('notify_type') == 'trade_status_sync' and request.POST.get('trade_status') == 'TRADE_SUCCESS'): #Alipay
        if checkin(transaction_id, userid, bank_type, otid) == 'success':
            return HttpResponse('Success')
    return HttpResponse('Ali Notify not recognized!')

@csrf_exempt
def payment_notify_wx(request):
    params = xml_to_dict(request.body)
    otid = params['out_trade_no']
    transaction_id = params['transaction_id']
    openid = params['openid']
    bank_type = params['bank_type']
    if params['return_code'] == 'SUCCESS': #Wxpay
        if checkin(transaction_id, openid, bank_type, otid) == 'success':
            return HttpResponse('<xml><return_code><![CDATA[SUCCESS]]></return_code><return_msg><![CDATA[OK]]></return_msg></xml>')
    return HttpResponse('WX Notify not recognized!')

def checkin(transaction_id, openid, bank_type, otid):
    try:
        rc = FunboxRecord.objects.get(orderid=otid)
    except:
        return 'Record not found'
    pr,pb = rc.detail.split("-")
    mid = rc.memberid
    pr = float(pr)
    pb = float(pb)
    income = pr + pb
    try:#商户入帐
        ret = FunboxMember.objects.get(memberid=mid)
    except:
        return 'Member not found'
    if ret.man == 0:
        if ret.jian != 0 and income >= ret.jian:
            m_return = int(random.random()*200)/100.0
        else:
            m_return = 0
    else:
        m_return = int(income/ret.man)*ret.jian
    m_realin = income - m_return
    ret.balance += m_realin
    ret.total += m_realin
    ret.save()
    #商户提醒
    body={"touser":ret.wxid,
          "template_id":template,
          "url":"",
          "topcolor":"#173177",
          "data":{
              "keyword1":{"value":str(datetime.datetime.now())[:-7],"color":"#173177"},
              "keyword2":{"value":bank_type,"color":"#173177"},
              "keyword3":{"value":str(m_realin),"color":"#173177"},
              "keyword4":{"value":mid,"color":"#173177"},
              "keyword5":{"value":transaction_id,"color":"#173177"}}}
    token = json.loads(urllib2.urlopen(access_url%(appid,secret)).read())['access_token']
    urllib2.urlopen(urllib2.Request(remind_url%token, json.dumps(body, ensure_ascii=False)))
    try:#消费者入帐
        ret1 = FunboxUser.objects.get(wxid=openid)
        ret1.total += pr
        ret1.balance += m_return - pb
        ret1.save()
    except:
        ret1 = FunboxUser(wxid=openid, type=1, jointime=str(datetime.date.today())) #新建支付宝用户
        ret1.total += pr
        ret1.balance += m_return - pb
        ret1.save()
    detail_str = u"商家实收"+str(m_realin)+u"返现"+str(m_return)+u"（"+str(pb)+u"来自余额）, 订单编号："+transaction_id
    rc.userid = ret1.userid
    rc.type = bank_type
    rc.detail = detail_str
    rc.amount = m_realin
    rc.status = 1
    rc.save()
    return 'success'

@csrf_exempt
def payable(request):
    pr = request.POST.get('pay_real')
    pb = request.POST.get('pay_balance')
    oid = request.POST.get('openid')
    #oid = 'oJlYMxBklb9U24rkVe5ESmZOkoGc'
    mid = request.POST.get('memberid')
    otid = mid+'-'+str(int(time.time())) #不能含有.
    if oid: #wxpy
        parameter = {
        'body': 'Jyousoft wxpay',
        'openid': oid,
        'out_trade_no': otid,
        'spbill_create_ip': request.META.get('REMOTE_ADDR', ''),
        'total_fee': str(int(float(pr)*100)),
        }
        parameter.update(pay_param)
        FunboxRecord(orderid=otid, memberid=mid, userid=0, type='wx', detail=pr+'-'+pb, amount=0, status=2).save()
        return HttpResponse(str(build_form(parameter)).replace(" u'", "'"))
    else: #alipay
        paybar = alipay.AliPay(appid=aliappid, app_notify_url=ali_notify_url, app_private_key_string=app_private_key_string, alipay_public_key_string=alipay_public_key_string, sign_type="RSA", debug=True)
        order_string = paybar.api_alipay_trade_wap_pay(
            out_trade_no=otid,
            total_amount=float(pr),
            subject='支付宝消费',
            return_url=return_url % mid)
        FunboxRecord(orderid=otid, memberid=mid, userid=0, type='alipay', detail=pr+'-'+pb, amount=0, status=2).save()
        return HttpResponse(aligateway+order_string)
