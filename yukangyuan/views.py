# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from yukangyuan.models import *
import xml.etree.ElementTree as ET
import share, hashlib, random, datetime
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
    return share.getTextXml(msg, u'谢谢您的留言，我们会尽快处理')

def login(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        cuser = '未登录'
    else:
        cuser = request.session['login_user']
    if 'old_user' in request.session and request.session['old_user']:
        ouser = request.session['old_user']
    else:
        ouser = ''
    context = { 'olduser': ouser, 'login_user': cuser }
    return render(request, 'yukangyuan/login.html', context)

@csrf_exempt
def dologin(request):
    userid = request.POST.get('userid')
    password = request.POST.get('password')
    type = request.POST.get('type')
    if type == '1':
        try:
            ret = YukangyuanSaler.objects.get(salerid=userid, password=password)
            request.session['login_user'] = ret.salerid
            if ret.salerid == 1:
                return redirect('/yukangyuan/summary/')
            else:
                return redirect('/yukangyuan/saler/')
        except:
            return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../login/"></head><h1>业务员登录失败</h1></html>''')
    else:
        try:
            ret = YukangyuanCustomer.objects.get(customerid=userid, password=password)
            request.session['login_user'] = ret.customerid
            return redirect('/yukangyuan/product/')
        except:
            return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../login/"></head><h1>商户登录失败</h1></html>''')

def logout(request):
    if 'login_user' not in request.session:
        request.session['old_user'] = ""
    else:
        request.session['old_user'] = request.session['login_user']
    request.session['login_user'] = ""
    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../login/"></head><h1>登出成功!</h1></html>''')

@csrf_exempt
def changepwd(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        return HttpResponse('请先登录')
    elif not request.POST.get('newpwd') == request.POST.get('againpwd'):
        return HttpResponse('两次密码不一致')
    else:
        try:
            ret = YukangyuanCustomer.objects.get(customerid=request.session['login_user'])
            ret.password = request.POST.get('newpwd')
            ret.save()
            return HttpResponse('商户密码修改成功')
        except:
            try:
                ret2 = YukangyuanSaler.objects.get(salerid=request.session['login_user'])
                ret2.password = request.POST.get('newpwd')
                ret2.save()
                return HttpResponse('业务员密码修改成功')
            except:
                HttpResponse('用户身份过期，请重新登录')

def product(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        return redirect('/yukangyuan/login/')
    if request.GET.get('customerid'):
        cid = request.GET.get('customerid')
    else:
        cid = request.session['login_user']
    customer = YukangyuanCustomer.objects.get(customerid=cid)
    cates = YukangyuanProduct.objects.values_list('brand', flat=True).distinct()
    cate = request.GET.get('cate')
    plist = []
    if cate:
        products = YukangyuanProduct.objects.filter(brand=cate).order_by('productid')
    else:
        products = YukangyuanProduct.objects.all().order_by('productid')
    for p in products:
        if p.flag in customer.privilege:
            plist.append({'productid':p.productid, 'code':p.code, 'name':p.name, 'type':p.type, 'storage':p.storage,
            'price':eval('p.price'+str(customer.grade)), 'pic':p.pic, 'detail':p.detail})
    context = { 'cgrade':customer.grade, 'cates':cates, 'customer':cid, 'products':plist, 'login_user':request.session['login_user'] }
    return render(request, 'yukangyuan/product.html', context)

@csrf_exempt
def addproduct(request):
    customerid = request.POST.get('customerid')
    productid = request.POST.get('productid')
    num = int(request.POST.get('num'))
    total = int(request.POST.get('price'))*num
    storage = YukangyuanProduct.objects.get(productid=productid).storage
    if num > storage:
        return HttpResponse('库存不足，请减少订货量重试')
    else:
        YukangyuanOrderdetail(customerid=customerid,productid=productid,amount=num,total=total,status=0).save()
        return HttpResponse('%s个共计%s元，下单成功' %(str(num), str(total)))

def customer(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        return redirect('/yukangyuan/login/')
    customerid = request.GET.get('customerid')
    ret = YukangyuanCustomer.objects.get(customerid=customerid)
    pending = []
    price = 0
    ismysaler = request.session['login_user']==ret.salerid
    if request.session['login_user']==customerid or ismysaler:
        for od in YukangyuanOrderdetail.objects.filter(customerid=customerid, status=0):
            prod = YukangyuanProduct.objects.get(productid=od.productid)
            pending.append({'detailid':od.detailid, 'code':prod.code, 'name':prod.name, 'number':od.amount, 'total':od.total})
            price += od.total
        context = { 'pending': pending,
                'ismysaler': ismysaler,
                'address': ret.address+u'，联系人：'+ret.contact+u'，电话：'+ret.phone,
                'price': price,
                'order': YukangyuanOrder.objects.filter(customerid=customerid).order_by('-date')[:40],
                'support': YukangyuanSupport.objects.filter(customerid=customerid).order_by('-date')[:20],
                'return': YukangyuanReturn.objects.filter(customerid=customerid).order_by('-date')[:20],
                'customer': customerid,
                'login_user': request.session['login_user'] }
    else:
        context = {'login_user':''}
    return render(request, 'yukangyuan/customer.html', context)

@csrf_exempt
def doorder(request):
    detailids = request.POST.getlist('detailids')
    cid = request.POST.get('customerid')
    total = int(request.POST.get('total'))
    if not len(detailids):
        return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>订单是空的</h1></html>''' %cid)
    if request.POST.get('cancel'):
        for i in detailids:
            YukangyuanOrderdetail.objects.get(detailid=int(i)).delete()
        return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>订单已取消</h1></html>''' %cid)
    if request.POST.get('confirm'):
        #if total < 1000:
        #    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>每笔订单最低1000元起</h1></html>''' %cid)
        if YukangyuanOrderdetail.objects.filter(customerid=cid, orderid=0):
            disc = request.POST.get('discount')
            if disc:
                try:
                    total *= float(disc)
                except:
                    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>减免必须为数字, 如0.9</h1></html>''' %cid)
            detail = u'配送信息：' + request.POST.get('address') + u'，备注：' + request.POST.get('note')
            newo = YukangyuanOrder(customerid=cid, total=total, detail=detail, status=1)
            newo.save()
            for i in detailids:
                ret = YukangyuanOrderdetail.objects.get(detailid=i)
                cp = YukangyuanProduct.objects.get(productid=ret.productid)
                cp.storage -= ret.amount
                cp.save()
                ret.orderid = newo.orderid
                ret.status = 1
                ret.save()
        return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>订单已确认</h1></html>''' %cid)

@csrf_exempt
def saler(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        return redirect('/yukangyuan/login/')    
    stime = request.POST.get('stime')
    etime = request.POST.get('etime')
    cname = request.POST.get('cname')
    brand = request.POST.get('brand')
    ptitle = request.POST.get('ptitle')
    cinfo = []
    customers = YukangyuanCustomer.objects.filter(salerid=request.session['login_user']) 
    if cname:
        customers = customers.filter(name__contains=cname)
    pool = YukangyuanProduct.objects.all()
    brands = pool.values_list('brand', flat=True).distinct()
    if brand:
        pool = pool.filter(brand=brand)
    supports = YukangyuanSupport.objects.all()
    returns = YukangyuanReturn.objects.all()
    if ptitle:
        supports = supports.filter(detail__contains=ptitle)
        returns = returns.filter(detail__contains=ptitle)
        pool = pool.filter(name__contains=ptitle)
    orders = YukangyuanOrderdetail.objects.filter(productid__in=pool.values_list('productid', flat=True))
    if stime:
        stime = datetime.datetime.strptime(stime, "%Y%m%d")
    else:
        stime = datetime.datetime.strptime('20170101', "%Y%m%d")
    orders = orders.filter(date__gt=stime)
    supports = supports.filter(date__gt=stime)
    returns = returns.filter(date__gt=stime)
    if etime:
        etime = datetime.datetime.strptime(etime, "%Y%m%d")
        orders = orders.filter(date__lt=etime)
        supports = supports.filter(date__lt=etime)
        returns = returns.filter(date__lt=etime)
    salertotal = 0
    for c in customers:
        o_num = 0
        o_total = 0
        s_num = 0
        s_total = 0
        r_num = 0
        r_total = 0
        for o in orders.filter(customerid=c.customerid):
            o_num += 1
            o_total += o.total
        for s in supports.filter(customerid=c.customerid):
            s_num += 1
            s_total += s.total
        for r in returns.filter(customerid=c.customerid):
            r_num += 1
            r_total += r.total
        cinfo.append({'b_num':o_num, 'a_total':o_total, 'cid':c.customerid, 'name':c.name, 's_num':s_num, 's_total':s_total, \
        'r_num':r_num, 'r_total':r_total})
        salertotal += o_total
    context = { 'brands':brands, 'cinfo':sorted(cinfo, reverse=True), 'salertotal':salertotal, 'login_user':request.session['login_user'] }
    return render(request, 'yukangyuan/saler.html', context)

@csrf_exempt
def addreport(request):
    salerid = request.POST.get('salerid')
    report = request.POST.get('report')
    if report:
        YukangyuanReport(salerid=salerid, content=report).save()
        return HttpResponse('报告提交成功！')
    else:
        return HttpResponse('报告不能为空！')

def summary(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        return redirect('/yukangyuan/login/')    
    uid = request.session['login_user']
    stime = request.POST.get('stime')
    etime = request.POST.get('etime')
    if not uid == 1:
        uid = ''
    sinfo = []
    reports = []
    current_year = datetime.datetime.now().year
    for s in YukangyuanSaler.objects.filter(salerid__gt=1):
        customers = YukangyuanCustomer.objects.filter(salerid=s.salerid)
        orders = YukangyuanOrder.objects.filter(customerid__in=customers.values_list('customerid', flat=True))
        supports = YukangyuanSupport.objects.filter(date__year=current_year, customerid__in=customers.values_list('customerid', flat=True))
        if stime:
            tag = datetime.datetime.strptime(stime, "%Y%m%d")
            orders = orders.filter(date__gt=tag)
            supports = supports.filter(date__gt=tag)
        if etime:
            tag = datetime.datetime.strptime(etime, "%Y%m%d")
            orders = orders.filter(date__lt=tag)
            supports = supports.filter(date__lt=tag)
        ototal = 0
        stotal = 0
        for o in orders:
            ototal += o.total
        for sp in supports:
            stotal += sp.total
        sinfo.append({'sname':s.name, 'sdes':s.description, 'onum':len(orders), 'ototal':ototal, 'snum':len(supports), 'stotal':stotal})
    for r in YukangyuanReport.objects.all().order_by('-date')[:20]:
        sname = YukangyuanSaler.objects.get(salerid=r.salerid).name
        reports.append({'sname':sname, 'content':r.content, 'date':r.date})
    context = { 'login_user':uid, 'sinfo':sinfo, 'reports':reports }
    return render(request, 'yukangyuan/summary.html', context)

def getdetail(request):
    orderid = request.GET.get('orderid')
    if request.GET.get('html'):
        rt = '<br/>'
    else:
        rt = '\n'
    ret = u'订单内容：' + rt
    for od in YukangyuanOrderdetail.objects.filter(orderid=orderid):
        prod = YukangyuanProduct.objects.get(productid=od.productid)
        ret += prod.code + ' - ' + prod.name + rt + 'X ' + str(od.amount) + u' 小计：￥' + str(od.total) + rt
    order = YukangyuanOrder.objects.get(orderid=orderid)
    ret += u'订单总计：￥' + str(order.total) + rt + rt.join(order.detail.split(u"，"))
    return HttpResponse(ret)

def deletedetail(request):
    detailid = request.GET.get('detailid')
    YukangyuanOrderdetail.objects.get(detailid=detailid).delete()
    return HttpResponse(u'删除成功')

def delorder(request):
    orderid = request.GET.get('orderid')
    for od in YukangyuanOrderdetail.objects.filter(orderid=orderid):
        od.delete()
    ret = YukangyuanOrder.objects.get(orderid=orderid)
    ret.delete()
    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>订单已撤消</h1></html>''' %ret.customerid)

@csrf_exempt
def dosupport(request):
    customerid = request.POST.get('customerid')
    detail = request.POST.get('detail')
    reason = request.POST.get('reason')
    total = request.POST.get('total')
    if total.isdigit():
        YukangyuanSupport(customerid=customerid, detail=detail, reason=reason, total=total).save()
        return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>市场支持成功</h1></html>''' %customerid)
    else:
        return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>支持价值必须为数字</h1></html>''' %customerid)

@csrf_exempt
def doreturn(request):
    customerid = request.POST.get('customerid')
    detail = request.POST.get('detail')
    reason = request.POST.get('reason')
    total = request.POST.get('total')
    if total.isdigit():
        YukangyuanReturn(customerid=customerid, detail=detail, reason=reason, total=total).save()
        return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>退货申请成功</h1></html>''' %customerid)
    else:
        return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../customer/?customerid=%s"></head><h1>退货价值必须为数字
</h1></html>''' %customerid)

