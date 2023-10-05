# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.utils.encoding import smart_str
from django.db.models import Q
from dfth.models import *
import share, hashlib, random, datetime

@csrf_exempt
def dologin(request):
    ac = request.POST.get('account')
    pw = str(request.POST.get('password'))
    try:
        request.session['login_user'] = DfthEmployee.objects.get(employeename=ac, password=pw)
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../"></head>登录成功</html>''')
    except:
        return HttpResponse('''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../"></head>密码错误</html>''')

def logout(request):
    request.session['login_user'] = ""
    return HttpResponse(u'''<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../"></head>登出成功!</html>''')

@csrf_exempt
def changepwd(request):
    if 'login_user' not in request.session or request.session['login_user']=='':
        return HttpResponse('请先登录')
    elif not request.POST.get('newpwd') == request.POST.get('againpwd'):
        return HttpResponse('两次密码不一致')
    else:
        try:
            ret = DfthEmployee.objects.get(employeename=request.session['login_user'].employeename)
            ret.password = request.POST.get('newpwd')
            ret.save()
            return HttpResponse('密码修改成功')
        except:
            HttpResponse('登录身份过期，请重新登录')

def index(request):
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    notice = DfthNotice.objects.all()
    if request.session['login_user']:
        expense = DfthExpense.objects.filter(username=request.session['login_user'].employeename)
    else:
        expense = ""
    context = { 'login_user': request.session['login_user'],
                'notice': notice,
                'expense': expense }
    return render(request, 'dfth/index.html', context)

def produce(request):
    word = request.POST.get('word')
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    source = DfthSource.objects.all()
    sale = DfthSale.objects.all().order_by('-id')
    product = DfthProduct.objects.all()
    consume = DfthConsume.objects.all().order_by('-id')
    employee = DfthEmployee.objects.all()
    produce = DfthProduce.objects.all().order_by('-id')
    contract = DfthContract.objects.all().order_by('-contractid')
    device = DfthDevice.objects.all()
    if word:
        source = source.filter(sourcename__contains=word)
        sale = sale.filter(Q(productname__productname__contains=word) | Q(customername__customername__contains=word))
        product = product.filter(productname__contains=word)
        consume = consume.filter(Q(sourcename__sourcename__contains=word) | Q(employeename__employeename__contains=word))
        produce = produce.filter(productname__productname__contains=word)
        device = device.filter(Q(deviceid__contains=word) | Q(devicename__contains=word))
    context = { 'login_user': request.session['login_user'],
                'source': source,
                'sale': sale[:30],
                'product': product,
                'consume': consume[:30],
                'employee': employee,
                'produce': produce[:30],
                'contract': contract,
                'device': device,
              }
    return render(request, 'dfth/produce.html', context)

def sale(request):
    word = request.POST.get('word')
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    product = DfthProduct.objects.all()
    customer = DfthCustomer.objects.all()
    contract = DfthContract.objects.all().order_by('-contractid')
    sale = DfthSale.objects.all().order_by('-id')
    if word:
        product = product.filter(productname__contains=word)
        customer = customer.filter(Q(customername__contains=word) | Q(contact__contains=word) | Q(address__contains=word))
        contract = contract.filter(Q(customername__customername__contains=word) | Q(summary__contains=word))
        sale = sale.filter(Q(productname__productname__contains=word) | Q(customername__customername__contains=word))
    context = { 'login_user': request.session['login_user'],
                'product': product,
                'customer': customer,
                'contract': contract,
                'sale': sale[:30],
              }
    return render(request, 'dfth/sale.html', context)

def finance(request):
    word = request.POST.get('word')
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    employee = DfthEmployee.objects.all()
    customer = DfthCustomer.objects.all().order_by('customername')
    contract = DfthContract.objects.all().order_by('-contractid')
    income = DfthIncome.objects.all().order_by('-id')
    expense = DfthExpense.objects.filter(status__lt=3)
    device = DfthDevice.objects.all()
    if word:
        customer = customer.filter(Q(customername__contains=word) | Q(contact__contains=word) | Q(address__contains=word))
        contract = contract.filter(Q(customername__customername__contains=word) | Q(summary__contains=word))
        income = income.filter(customername__customername__contains=word)
        expense = expense.filter(Q(username__contains=word) | Q(type__contains=word) | Q(reason__contains=word))
        device = device.filter(Q(deviceid__contains=word) | Q(devicename__contains=word))
    context = { 'login_user': request.session['login_user'],
                'employee': employee,
                'customer': customer,
                'contract': contract[:30],
                'income': income[:30],
                'expense': expense,
                'device': device,
              }
    return render(request, 'dfth/finance.html', context)

def purchase(request):
    word = request.POST.get('word')
    if 'login_user' not in request.session:
        request.session['login_user'] = ""
    source = DfthSource.objects.all()
    supplyer = DfthSupplyer.objects.all().order_by('supplyername')
    purchase = DfthPurchase.objects.all().order_by('-id')
    if word:
        source = source.filter(sourcename__contains=word)
        supplyer = supplyer.filter(Q(supplyername__contains=word) | Q(address__contains=word))
        purchase = purchase.filter(Q(supplyername__supplyername__contains=word) | Q(sourcename__sourcename__contains=word))
    context = { 'login_user': request.session['login_user'],
                'source': source,
                'supplyer': supplyer,
                'purchase': purchase[:30],
              }
    return render(request, 'dfth/purchase.html', context)

def addconsume(request):
    sourcename = request.POST.get('sourcename')
    employeename = request.POST.get('employeename')
    number = request.POST.get('number')
    if sourcename == "" or employeename == "" or number == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../produce"></head>所有信息须填写完整正确</html>')
    source = DfthSource.objects.get(sourcename=sourcename)
    number = float(number)
    if number > source.number:
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../produce"></head>所需库存不足，请联系管理员</html>')
    employee = DfthEmployee.objects.get(employeename=employeename)
    DfthConsume(sourcename=source, employeename=employee, number=number).save()
    source.number -= number
    source.save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../produce"></head>原料领用信息添加成功</html>')

def addproduce(request):
    productname = request.POST.get('productname')
    number = request.POST.get('number')
    if productname == "" or number == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../produce"></head>所有信息须填写完整正确</html>')
    product = DfthProduct.objects.get(productname=productname)
    if product.productname in (u'安尼优-N',u'安尼优-N50',u'安尼优-C',u'安尼优-M',u'安尼优-L'):
        keepdate = datetime.datetime.today()+datetime.timedelta(days=360)
    else:
        keepdate = datetime.datetime.today()+datetime.timedelta(days=180)
    DfthProduce(productname=product, keepdate=keepdate.strftime('%Y%m%d'), number=int(number)).save()
    product.number += int(number)
    product.save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../produce"></head>产出信息添加成功</html>')

def addcustomer(request):
    customername = request.POST.get('customername')
    type = request.POST.get('type')
    district = request.POST.get('district')
    location = request.POST.get('location')
    contact = request.POST.get('contact')
    phone = request.POST.get('phone')
    address = request.POST.get('address')
    invoiceinfo = request.POST.get('invoiceinfo')
    if customername == "" or contact == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../sale"></head>所有信息须填写完整正确</html>')
    DfthCustomer(customername=customername, type=type, district=district, location=location, contact=contact, phone=phone, address=address, invoiceinfo=invoiceinfo).save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../sale"></head>客户信息添加成功</html>')

def addcontract(request):
    contractid = request.POST.get('contractid')
    customername = request.POST.get('customername')
    summary = request.POST.get('summary')
    total = request.POST.get('total')
    if contractid == "" or customername == "" or total == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../sale"></head>所有信息须填写完整正确</html>')
    customer = DfthCustomer.objects.get(customername=customername)
    DfthContract(contractid=contractid, customername=customer, summary=summary, total=int(total)).save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../sale"></head>合同信息添加成功</html>')

def addsale(request):
    contractid = request.POST.get('contractid')
    productname = request.POST.get('productname')
    keepdate = request.POST.get('keepdate')
    number = request.POST.get('number')
    price = request.POST.get('price')
    if contractid == "" or productname == "" or number == "" or price == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../sale"></head>销售信息须填写完整正确</html>')
    contract = DfthContract.objects.get(contractid=contractid)
    product = DfthProduct.objects.get(productname=productname)
    if int(number) > product.number:
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../sale"></head>所需库存不足，请联系管理员</html>')
    DfthSale(contractid=contract, customername=contract.customername, productname=product, keepdate=keepdate, number=int(number), price=float(price)).save()
    product.number -= int(number)
    product.save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../sale"></head>销售信息添加成功</html>')

def addpurchase(request):
    supplyername = request.POST.get('supplyername')
    sourcename = request.POST.get('sourcename')
    location = request.POST.get('location')
    keepdate = request.POST.get('keepdate')
    number = request.POST.get('number')
    price = request.POST.get('price')
    if supplyername == "" or sourcename == "" or number == "" or price == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../purchase"></head>所有信息须填写完整正确</html>')
    source = DfthSource.objects.get(sourcename=sourcename)
    supplyer = DfthSupplyer.objects.get(supplyername=supplyername)
    DfthPurchase(supplyername=supplyer, sourcename=source, location=location, keepdate=keepdate, number=float(number), price=float(price)).save()
    source.number += float(number)
    source.save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../purchase"></head>原料采购信息添加成功</html>')

def addincome(request):
    contractid = request.POST.get('contractid')
    number = request.POST.get('number')
    if contractid == "" or number == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../finance"></head>所有信息须填写完整正确</html>')
    try:
        contract = DfthContract.objects.get(contractid=contractid)
    except:
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../finance"></head>此合同号未找到</html>')
    DfthIncome(customername=contract.customername, contractid=contract, number=int(number)).save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../finance"></head>收入信息添加成功</html>')

def addexpense(request):
    username = request.POST.get('username')
    type = request.POST.get('type')
    reason1 = request.POST.get('reason1')
    reason2 = request.POST.get('reason2')
    number = request.POST.get('number')
    if not username:
        username = "财务"
    if type == "" or reason2 == "" or number == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../"></head>所有信息须填写完整正确</html>')
    DfthExpense(username=username, type=type, reason=reason1+u"  收款人："+reason2, status=0, number=float(number)).save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../"></head>支出信息添加成功</html>')

def addsupplyer(request):
    supplyername = request.POST.get('supplyername')
    address = request.POST.get('address')
    phone = request.POST.get('phone')
    if supplyername == "" or address == "" or phone == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../purchase"></head>所有信息须填写完整正确</html>')
    DfthSupplyer(supplyername=supplyername, address=address, phone=phone).save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../purchase"></head>供应商信息添加成功</html>')

def addsource(request):
    sourcename = request.POST.get('sourcename')
    type = request.POST.get('type')
    if sourcename == "" or type == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../purchase"></head>所有信息须填写完整正确</html>')
    DfthSource(sourcename=sourcename, type=type, number=0).save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../purchase"></head>原料信息添加成功</html>')

def adddevice(request):
    deviceid = request.POST.get('deviceid')
    devicename = request.POST.get('devicename')
    buydate = request.POST.get('buydate')
    price = request.POST.get('price')
    if deviceid == "" or devicename == "" or price == "":
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="2;URL=../finance"></head>所有信息须填写完整正确</html>')
    DfthDevice(deviceid=deviceid, devicename=devicename, buydate=buydate, price=int(price)).save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../finance"></head>设备信息添加成功</html>')

def approvesubmit(request):
    eid = request.GET.get('eid')
    action = request.GET.get('action')
    ret = DfthExpense.objects.get(id=eid)
    ret.status = action
    ret.save()
    return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="1;URL=../finance/"></head>操作成功</html>')
