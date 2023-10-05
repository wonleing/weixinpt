# -*- coding: utf-8 -*-
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate
from django.conf import settings
from django.utils.encoding import smart_str
from live_hk.models import *
import MySQLdb, random, time, datetime, urllib2

footer = '''</ul></div></div></body><script type="text/javascript" src="../../static/js/iScroll.js"></script>
    <script type="text/javascript" src="../../static/js/style.js"></script>
</html>
'''

def index(request):
    return HttpResponse("""<h1>本平台由<a href="http://www.jyousoft.com/">捷优软件</a>提供</h1>
    <h2>联系邮箱wonleing@jyousoft.com, 咨询电话13810776712</h2>
    <a href="http://zhanzhang.anquan.org/physical/report/?domain=weixinpt.sinaapp.com" name="sK2tBF0FLYDRj4cRrm20iJbNPCb2gwdaFTB8lfHmcQuir6Xtg4"><img height="47" src="http://zhanzhang.anquan.org/static/common/images/zhanzhang.png"alt="安全联盟站长平台" /></a>
    <script type="text/javascript" src="http://www.hbwj.gov.cn:80/hbwjww/VieidServlet?webId=2b931791437294c22350d2e974a17f38&width=100&heigth=130"></script>
    """)

def upload(request):
    return render(request, 'upload.html')

def verify(request):
    return HttpResponse('202203240920176a1s5sofdhqsbfh3sidt9zhyhpa8kkv90yfhxrqi6wkx9zkp3f')
    return HttpResponse('IhKTFj6rjwwxC76n')

def doupload(request):
    logined = 0
    ac = request.POST.get('ac')
    pw = request.POST.get('pw')
    if authenticate(username=ac, password=pw):
        try:
            file = request.FILES['filepath']
        except:
            return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="3;URL=/upload"></head>请选择上传文件</html>')
        tablename = file.readline().strip()
        columns = file.readline().strip()
        if ac != 'leon' and ac not in tablename:
            return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="3;URL=/upload"></head>该用户无权操作此表，请检查表名</html>')
        sql = 'insert into %s %s values ' %(tablename, columns)
        entry = []
        for line in file.readlines():
            try:
                line = line.decode('gb18030').encode('utf8')
            except:
                pass
            if line and line[0] != '#':
                entry.append('("'+'","'.join(line.strip().split("|"))+'")')
        sql += ",".join(entry)
        con = MySQLdb.connect(host=settings.MYSQL_HOST_M, user=settings.MYSQL_USER, passwd=settings.MYSQL_PASS, db=settings.MYSQL_DB, \
        port=int(settings.MYSQL_PORT))
        con.set_character_set('UTF8')
        cur = con.cursor()
        #cur.execute('delete from %s' %tablename)
        try:
            cur.execute(sql)
        except:
            return HttpResponse('导入错误，调试信息：%s' % sql)
        con.commit()
        con.close()
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="3;URL=/upload"></head>导入成功</html>')
    else:
        return HttpResponse('<html><head><META HTTP-EQUIV="refresh" CONTENT="3;URL=/upload"></head>用户名密码错误</html>')

def hongbao(bid, openid):
    try:
        aw = LiveHkAward.objects.get(bid=bid)
    except:
        return u'活动设置中还没有此项活动'
    ret = LiveHkRecord.objects.filter(name=openid, phone=bid, type=aw.type)
    if ret:
        return u'你已经领过这个红包了'
    LiveHkRecord(name=openid, phone=bid, type=aw.type, date=datetime.date.today().isoformat()).save()
    if aw.rate != 0 and aw.amount > 0 and random.random()*aw.rate < 1:
        aw.amount -= 1
        aw.save()
        money = random.randint(100, aw.point)
        res = urllib2.urlopen(aw.link+"?wxid="+openid+"&amount="+str(money)).read()
        return res
    else:
        return u'手气差了点，谢谢您的分享'

def header(cssfile):
    return '''<html>
    <head>
        <meta http-equiv=Content-Type content="text/html;charset=utf-8">
        <meta name="viewport" content="width=device-width, minimum-scale=1.0,maximum-scale=1.0,user-scalable=no">
        <meta name="apple-mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black">
        <meta name="format-detection" content="telephone=no">
        <link href="%s" rel="stylesheet" type="text/css" />
    </head>\n''' %cssfile

def randomreply(tbname, line=None):
    pool = [u'您要查询什么信息？%s',u'您的回复我看不懂唉，试试%s',u'我太笨了...只能%s',u'别再逗我了，%s',
    u'我是快乐机器人，%s',u'还有什么需要吗？%s',u'你很喜欢聊天吧，%s']
    menu = ""
    i = 0
    for item in tbname.objects.all().order_by('id'):
        menu += str(item.id) + u" " + item.title + u"\x0a"
        i += 1
    part = u'回复数字0显示主页面,回复数字1-%d查看分类页面:\x0a%s其它功能说明:\x0a' % (i, menu)
    if line:
        return line + '\x0a' + part
    else:
        return random.sample(pool,1)[0] % part

def msgpage(tbname):
    ret = u'<h1>互动留言</h1><p>直接在微信中按要求格式输入便可将您的留言在这里显示</p><hr/>'
    for m in tbname.objects.all().order_by('-id')[:1000]:
        try:
            m.content = m.contact + u'：' + m.content
        except:
            pass
        ret += u'<p>%s</p>' %m.content
        if m.reply:
            ret += u'<p>&emsp;<font color="#C00000">回复：</font>%s</p>' %m.reply
    ret += '<hr/>'
    return ret

def sublayout(item):
    if not item.link:
        item.link = ""
    if item.pic and len(item.description) < 150:
        ret = '''        <li><a href="%s">
        <div class="left parts_1"><img src="%s" /></div>
        <div class="right parts_2">\n''' %(item.link,item.pic)
    else:
        ret = '        <li><a href="%s"><div class="news">\n' %item.link
        if item.pic:
            ret += '       <img src="%s" /><br/>\n' %item.pic
    ret += '        <p>%s</p>\n' % item.title
    try:
        if item.price:
            ret += u"        <span>￥%s</span>\n" % item.price
    except:
        pass
    ret += '        <article>%s</article></div></a></li>\n' % "<br/>".join(item.description.split(" "))
    return ret

def submenu(tbname):
    subs = tbname.objects.all().order_by('id')
    ret = '        <div class="category" id="category">\n'
    for s in subs:
        ret += '            <li><a href="../%d">%s</a></li>\n' %(s.id, s.title)
    ret += '        </div>\n'
    return ret

def paraseMsgXml(rootElem):
    msg = {}
    if rootElem.tag == 'xml':
        for child in rootElem:
            msg[child.tag] = smart_str(child.text)
    return msg

def getTextXml(msg,replyContent):
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[text]]></MsgType><Content><![CDATA[%s]]></Content><FuncFlag>0</FuncFlag></xml>"
    extTpl = extTpl % (msg['FromUserName'],msg['ToUserName'],str(int(time.time())),replyContent)
    return extTpl

def getSingleXml(msg,title,des,pic,link=""):
    if not link:
        link = pic
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[news]]></MsgType><ArticleCount>1</ArticleCount><Articles><item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item></Articles></xml>" %(msg['FromUserName'],msg['ToUserName'],str(int(time.time())),title, des, pic, link)
    return extTpl

def getMultiXml(msg,title,list):
    extTpl = "<xml><ToUserName><![CDATA[%s]]></ToUserName><FromUserName><![CDATA[%s]]></FromUserName><CreateTime>%s</CreateTime><MsgType><![CDATA[news]]></MsgType>" %(msg['FromUserName'],msg['ToUserName'],str(int(time.time())))
    if title:
        if len(list) > 9:
            lth = 9
        else:
            lth = len(list)
        extTpl += "<ArticleCount>%d</ArticleCount><Articles><item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>" % (lth+1, title[0], title[1], title[2], title[3])
    else:
        if len(list) > 10:
            lth = 10
        else:
            lth = len(list)
        extTpl += "<ArticleCount>%d</ArticleCount><Articles>" % lth
    for item in list[:lth]:
        try:
            if item.price:
                item.title += u" ￥" + item.price
        except:
            pass
        if not item.link:
            item.link = ""
        extTpl += "<item><Title><![CDATA[%s]]></Title><Description><![CDATA[%s]]></Description><PicUrl><![CDATA[%s]]></PicUrl><Url><![CDATA[%s]]></Url></item>" % (item.title, item.description.replace("^", "\x0a"), item.pic, item.link)
    extTpl += "</Articles><FuncFlag>1</FuncFlag></xml>"
    return extTpl
