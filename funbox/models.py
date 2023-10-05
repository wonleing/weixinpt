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

class FunboxMsg(models.Model):
    memberid = models.CharField('会员ID', max_length=50L)
    amount = models.FloatField('提现金额', default=0)
    accountinfo = models.CharField('到账账号', max_length=500L, blank=True, null=True)
    date = models.DateTimeField('申请日期', auto_now=True)
    status = models.IntegerField('提现状态', choices=((0, '申请中'), (1, '已完成')))
    class Meta:
        verbose_name_plural = '提现申请'
        verbose_name = '提现申请'
        db_table = 'funbox_msg'
    def __unicode__(self):
        return self.memberid

class FunboxComment(models.Model):
    commentid = models.AutoField('评论号', primary_key=True)
    memberid = models.CharField('所属店铺', max_length=50L)
    userid = models.IntegerField('用户号')
    content = models.CharField('评论内容', max_length=500L, blank=True, null=True)
    status = models.IntegerField('评星')
    date = models.DateTimeField('评论日期', auto_now=True)
    tip = models.IntegerField('打赏', default=0)
    class Meta:
        verbose_name_plural = '评论'
        verbose_name = '评论'
        db_table = 'funbox_comment'
    def __unicode__(self):
        return str(self.commentid)

class FunboxUser(models.Model):
    userid = models.AutoField('用户号', primary_key=True)
    wxid = models.CharField('微信ID', max_length=50L, blank=True, null=True)
    password = models.CharField('密码', max_length=50L, blank=True, null=True)
    type = models.IntegerField('用户类型', choices=((0, '微信'), (1, '支付宝')))
    name = models.CharField('姓名', max_length=200L, blank=True, null=True)
    phone = models.CharField('电话', max_length=20L, blank=True, null=True)
    description = models.CharField('描述', max_length=500L, blank=True, null=True)
    pic = models.CharField('头像', max_length=200L, default='http://ww3.sinaimg.cn/mw690/558fe6e3gw1f10cjzp6u3j208c08cq38.jpg')
    balance = models.FloatField('余额', default=0)
    total = models.FloatField('累计消费', default=0)
    jointime = models.CharField('加入时间', max_length=20L, blank=True, null=True)
    class Meta:
        verbose_name_plural = '用户信息'
        verbose_name = '用户信息'
        db_table = 'funbox_user'
    def __unicode__(self):
        return str(self.userid)

class FunboxMember(models.Model):
    memberid = models.CharField('商户ID', primary_key=True, max_length=50L)
    wxid = models.CharField('微信ID', max_length=50L, blank=True, null=True)
    password = models.CharField('密码', max_length=50L, blank=True, null=True)
    type = models.IntegerField('商户类型', choices=((0,'代理'),(1,'购物'),(2,'美食'),(3,'丽人'),(4,'旅行'),(5,'休闲'),(6,'其它')))
    name = models.CharField('名称', max_length=200L, blank=True, null=True)
    phone = models.CharField('电话', max_length=20L, blank=True, null=True)
    address = models.CharField('地址', max_length=500L, blank=True, null=True)
    description = models.CharField('描述', max_length=500L, blank=True, null=True)
    accountinfo = models.CharField('提现账号', max_length=500L, blank=True, null=True)
    pic = models.CharField('商户主图', max_length=200L, default='http://ww2.sinaimg.cn/mw690/558fe6e3gw1f10ck076loj20hs0a0js1.jpg')
    logo = models.CharField('圆形logo', max_length=200L, default='http://ww1.sinaimg.cn/mw690/558fe6e3jw1f0l6989qcpj20t60t6409.jpg')
    balance = models.FloatField('余额', default=0)
    total = models.FloatField('累计收入', default=0)
    man = models.FloatField('满', default=0)
    jian = models.FloatField('减', default=0)
    fromagent = models.CharField('来自代理商', max_length=50L, blank=True, null=True)
    jointime = models.CharField('加入时间', max_length=20L, blank=True, null=True)
    class Meta:
        verbose_name_plural = '商户信息'
        verbose_name = '商户信息'
        db_table = 'funbox_member'
    def __unicode__(self):
        return self.memberid

class FunboxRecord(models.Model):
    orderid = models.CharField('订单ID', primary_key=True, max_length=50L) 
    memberid = models.CharField('商户ID', max_length=50L)
    userid = models.IntegerField('顾客ID')
    type = models.CharField('收入类型', max_length=50L)
    detail = models.CharField('交易详情', max_length=5000L)
    amount = models.FloatField('收入金额', default=0)
    date = models.DateTimeField('日期', auto_now=True)
    status = models.IntegerField('订单状态', choices=((0, '已退款'), (1, '已入帐'), (2, '未付款')))
    class Meta:
        verbose_name_plural = '收入记录'
        verbose_name = '收入记录'
        db_table = 'funbox_record'
    def __unicode__(self):
        return self.memberid

class FunboxAward(models.Model):
    level = models.IntegerField('等级', primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True, null=True)
    description = models.CharField('描述', max_length=1000L, blank=True, null=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True, null=True)
    link = models.CharField('链接URL', max_length=200L, blank=True, null=True)
    type = models.CharField('类型', max_length=200L, blank=True, null=True)
    rate = models.IntegerField('几率', blank=False)
    point = models.IntegerField('奖励', blank=False)
    amount = models.IntegerField('数量', default=0)
    class Meta:
        verbose_name_plural = '抽奖设置'
        verbose_name = '抽奖设置'
        db_table = 'funbox_award'
    def __unicode__(self):
        return self.title
