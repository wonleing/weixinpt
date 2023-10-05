# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from django.db import models

class JypayMsg(models.Model):
    centerid = models.CharField('商户ID', max_length=50L)
    memberid = models.CharField('渠道ID', max_length=50L)
    amount = models.FloatField('结算金额', default=0)
    accountinfo = models.CharField('到账账号', max_length=500L, blank=True, null=True)
    date = models.DateTimeField('结算日期', auto_now=True)
    class Meta:
        verbose_name_plural = '结算记录'
        verbose_name = '结算记录'
        db_table = 'jypay_msg'
    def __unicode__(self):
        return self.memberid

class JypayComment(models.Model):
    commentid = models.AutoField('评论号', primary_key=True)
    memberid = models.CharField('所属渠道', max_length=50L)
    userid = models.IntegerField('用户号')
    content = models.CharField('评论内容', max_length=500L, blank=True, null=True)
    status = models.IntegerField('评星')
    date = models.DateTimeField('评论日期', auto_now=True)
    tip = models.IntegerField('打赏', default=0)
    class Meta:
        verbose_name_plural = '评论'
        verbose_name = '评论'
        db_table = 'jypay_comment'
    def __unicode__(self):
        return str(self.commentid)

class JypayUser(models.Model):
    userid = models.AutoField('用户号', primary_key=True)
    wxid = models.CharField('微信ID', max_length=50L, blank=True, null=True)
    password = models.CharField('密码', max_length=50L, blank=True, null=True)
    type = models.IntegerField('用户类型', choices=((0, '微信'), (1, '支付宝')))
    name = models.CharField('姓名', max_length=200L, blank=True, null=True)
    phone = models.CharField('电话', max_length=20L, blank=True, null=True)
    description = models.CharField('描述', max_length=500L, blank=True, null=True)
    pic = models.CharField('头像', max_length=200L, default='https://up.enterdesk.com/edpic/b3/d6/2e/b3d62ef41f0bb610a69a7d6041e38a71.jpg')
    balance = models.FloatField('余额', default=0)
    total = models.FloatField('累计消费', default=0)
    jointime = models.CharField('加入时间', max_length=20L, blank=True, null=True)
    class Meta:
        verbose_name_plural = '用户信息'
        verbose_name = '用户信息'
        db_table = 'jypay_user'
    def __unicode__(self):
        return str(self.userid)

class JypayMember(models.Model):
    memberid = models.CharField('渠道ID', primary_key=True, max_length=50L)
    wxid = models.CharField('微信ID', max_length=50L, blank=True, null=True)
    password = models.CharField('密码', max_length=50L, blank=True, null=True)
    type = models.IntegerField('渠道分类', default=1)
    name = models.CharField('名称', max_length=200L, blank=True, null=True)
    phone = models.CharField('电话', max_length=20L, blank=True, null=True)
    address = models.CharField('地址或特点', max_length=500L, blank=True, null=True)
    description = models.CharField('详情', max_length=500L, blank=True, null=True)
    accountinfo = models.CharField('帐户信息', max_length=500L, blank=True, null=True)
    pic = models.CharField('主图', max_length=200L, default='https://i.328888.xyz/2023/01/05/WRn0o.jpeg')
    balance = models.FloatField('余额', default=0)
    total = models.FloatField('累计收入', default=0)
    fromagent = models.CharField('所属商户', max_length=50L, blank=True, null=True)
    jointime = models.CharField('加入时间', max_length=20L, blank=True, null=True)
    class Meta:
        verbose_name_plural = '渠道信息'
        verbose_name = '渠道信息'
        db_table = 'jypay_member'
    def __unicode__(self):
        return self.memberid

class JypayCenter(models.Model):
    centerid = models.CharField('商户ID', primary_key=True, max_length=50L)
    limit = models.IntegerField('用户上限', default=10)
    wxid = models.CharField('微信ID', max_length=50L, blank=True, null=True)
    password = models.CharField('密码', max_length=50L, blank=True, null=True)
    name = models.CharField('名称', max_length=200L, blank=True, null=True)
    phone = models.CharField('电话', max_length=20L, blank=True, null=True)
    description = models.CharField('详情', max_length=500L, blank=True, null=True)
    type1 = models.CharField('分类名1', max_length=20L, default='-')
    type2 = models.CharField('分类名2', max_length=20L, default='-')
    type3 = models.CharField('分类名3', max_length=20L, default='-')
    type4 = models.CharField('分类名4', max_length=20L, default='-')
    type5 = models.CharField('分类名5', max_length=20L, default='-')
    type6 = models.CharField('分类名6', max_length=20L, default='-')
    appid = models.CharField('APPID', max_length=50L, blank=True, null=True)
    secret = models.CharField('SECRET', max_length=50L, blank=True, null=True)
    mch_id = models.CharField('MCH_ID', max_length=50L, blank=True, null=True) 
    partnerkey = models.CharField('PARTENERKEY', max_length=50L, blank=True, null=True) 
    wxtemplate = models.CharField('TEMPLATE', max_length=500L, blank=True, null=True)
    aliappid = models.CharField('ALIAPPID', max_length=50L, blank=True, null=True)
    aliprivate = models.CharField('ALIPRIVATE', max_length=1500L, blank=True, null=True)
    alipublic = models.CharField('ALIPUBLIC', max_length=500L, blank=True, null=True)         
    cssfile = models.CharField('CSSFILE', max_length=200L, default="/static/css/jy.css")
    logo = models.CharField('商户logo', max_length=200L, default='https://i.328888.xyz/2023/01/05/WRn0o.jpeg')
    pic = models.CharField('关注海报', max_length=200L, default='https://pic.rmb.bdstatic.com/bjh/events/e21b7a318df37bed2c0b136dd1b07e16.jpeg')
    balance = models.FloatField('未结算额', default=0)
    total = models.FloatField('累计收入', default=0)
    man = models.FloatField('满', default=0)
    jian = models.FloatField('减', default=0)
    endtime = models.CharField('到期时间', max_length=20L, blank=True, null=True)
    class Meta:
        verbose_name_plural = '商户信息'
        verbose_name = '商户信息'
        db_table = 'jypay_center'
    def __unicode__(self):
        return self.centerid

class JypayRecord(models.Model):
    orderid = models.CharField('订单ID', primary_key=True, max_length=50L) 
    memberid = models.CharField('渠道ID', max_length=50L)
    userid = models.IntegerField('顾客ID')
    type = models.CharField('收入类型', max_length=50L)
    detail = models.CharField('交易详情', max_length=500L)
    amount = models.FloatField('收入金额', default=0)
    date = models.DateTimeField('日期', auto_now=True)
    status = models.IntegerField('订单状态', choices=((0, '已退款'), (1, '已入帐'), (2, '未付款')))
    class Meta:
        verbose_name_plural = '收入记录'
        verbose_name = '收入记录'
        db_table = 'jypay_record'
    def __unicode__(self):
        return self.memberid
