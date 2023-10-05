# encoding=utf-8
import hashlib, json, urllib, urllib2, time 
from random import Random
from django.utils.encoding import smart_str, smart_unicode
import xml.etree.ElementTree as ET

DELIVER_NOTIFY_URL = 'https://api.weixin.qq.com/pay/delivernotify'
ORDER_QUERY_URL = 'https://api.weixin.qq.com/pay/orderquery'
ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/cgi-bin/token'
base = {
    'trade_type': 'JSAPI',
    'sign_type': 'MD5'
}
filterKeys = ['appId', 'mch_id', 'openid', 'nonce_str', 'body', 'out_trade_no', 'total_fee', 'spbill_create_ip', 'notify_url', 'trade_type']
payKeys = ['appId', 'timeStamp', 'nonceStr', 'package', 'signType']

def build_form(parameter):
    parameter['nonce_str'] = random_str()
    parameter['timestamp'] = str(int(time.time()))
    parameter.update(base)
    parameter['sign'] = build_ordersign(parameter)
    paydic = {'appId':parameter['appId'], 'timeStamp':parameter['timestamp'], 'nonceStr':parameter['nonce_str'], 'package':"prepay_id=" + str(build_package(parameter)), 'signType':parameter['sign_type']}
    paydic['paySign'] = build_paysign(paydic, parameter['partnerKey'])
    return paydic

def build_package(parameter):
    pkeys = filterKeys + ['sign']
    url = 'https://api.mch.weixin.qq.com/pay/unifiedorder'
    r = ET.Element("xml")
    for (k, v) in parameter.items():
        if k in pkeys:
            key=ET.SubElement(r, k.lower())
            key.text=v
    data = ET.tostring(r, 'utf-8') 
    res = xml_to_dict(do_post(url, data))
    #req = urllib2.Request(url) 
    #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    #res =  xml_to_dict(opener.open(req, data).read())
    #return res #for debuging
    if res['return_code'] == u'FAIL':
        return res['return_msg']
    else:
        return res['prepay_id']

def verify_notify(params):
    wx_sign = params['sign']
    joined_string = '&'.join(['%s=%s' % (key.lower(), unicode(params[key])) for key in filterKeys])
    joined_string += '&key=' + params['partnerKey']
    m = hashlib.md5(joined_string.encode('utf-8'))
    m.digest()
    sign = m.hexdigest().upper()
    return wx_sign == sign

def build_ordersign(parameter):
    filterKeys.sort()
    joined_string = '&'.join(['%s=%s' % (key.lower(), parameter[key]) for key in filterKeys])
    joined_string += '&key=' + parameter['partnerKey']
    sign = hashlib.md5(joined_string).hexdigest().upper()
    return sign

def build_paysign(parameter, partnerkey):
    payKeys.sort()
    joined_string = '&'.join(['%s=%s' % (key, parameter[key]) for key in payKeys])
    joined_string += '&key=' + partnerkey
    sign = hashlib.md5(joined_string).hexdigest().upper()
    return sign

def get_access_token():
    token_url = ACCESS_TOKEN_URL + '?grant_type=client_credential&appid=' + parameter['appId'] + '&secret=' + parameter['appSecret']
    urlopen = urllib2.urlopen(token_url, timeout=12000)
    result = urlopen.read()
    data = json.loads(result)
    if 'errcode' in data:
        return False
    return data['access_token']

def order_query(out_trade_no):
    if config != None or out_trade_no != None:
        return False
    url = ORDER_QUERY_URL + '?access_token=' + get_access_token()
    parameter.update({
        'package': 'out_trade_no=' + out_trade_no +
                   '&partner=' + parameter['partnerId'] +
                   '&sign=' + (hashlib.md5('out_trade_no=' + out_trade_no +
                                           '&partner=' + parameter['partnerId'] +
                                           '&key=' + config['partnerkey'])).lower(),
        'timestamp': int(time.time())
    })
    parameter['app_signature'] = build_ordersign(parameter)
    parameter['sign_method'] = 'md5'
    result = do_post(url, parameter)
    return json.load(result)

def do_post(url, parameter):
    req = urllib2.Request(url)
    #enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, json.dumps(parameter))
    return response.read()

def random_str(randomlength=32):
    str = ''
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str

def xml_to_dict(raw_str):
    raw_str = smart_str(raw_str)
    msg = {}
    root_elem = ET.fromstring(raw_str)
    if root_elem.tag == 'xml':
        for child in root_elem:
            msg[child.tag] = smart_unicode(child.text)
        return msg
    else:
        return None
