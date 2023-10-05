# -*- coding: utf-8 -*-
from django.db import models

class XgxmMember(models.Model):
    memberid = models.CharField('代号', max_length=50L, primary_key=True)
    name = models.CharField('全称', max_length=50L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    otherpic = models.CharField('更多图片', max_length=2000L, blank=True)
    detail = models.CharField('详细介绍', max_length=5000L, blank=True)
    address = models.CharField('地址', max_length=500L, blank=True)
    lat = models.FloatField('纬度', blank=True)
    lon = models.FloatField('经度', blank=True)
    phone = models.CharField('电话', max_length=20L, blank=True)
    contact = models.CharField('联系人', max_length=20L, blank=True)
    level = models.IntegerField('优先级', default=0)
    class Meta:
        verbose_name_plural = '代理商(预留)'
        verbose_name = '代理商(预留)'
        db_table = 'xgxm_member'
    def __unicode__(self):
        return self.memberid

class XgxmProduct(models.Model):
    productid = models.AutoField('产品编号', primary_key=True)
    level = models.IntegerField('优先级', default=0)
    type = models.IntegerField('分类', default=1)
    title = models.CharField('产品名称', max_length=50L)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    otherpic = models.CharField('轮播图或视频', max_length=2000L, blank=True)
    price = models.FloatField('价格', default=0)
    tag = models.CharField('标签', max_length=50L, blank=True)
    onsale = models.IntegerField('商城在售', choices=((0, '否'), (1, '是')), default=0)
    class Meta:
        verbose_name_plural = '产品列表'
        verbose_name = '产品列表'
        db_table = 'xgxm_product'
    def __unicode__(self):
        return str(self.productid) + "-" + self.title

class XgxmUser(models.Model):
    userid = models.AutoField('用户编号', primary_key=True)
    wxid = models.CharField('微信ID', max_length=50L, blank=True)
    name = models.CharField('用户昵称', max_length=50L, blank=True)
    detail = models.CharField('用户描述', max_length=500L, blank=True)
    pic = models.CharField('头像地址', max_length=500L, blank=True)
    address = models.CharField('收货信息', max_length=500L, blank=True)
    token = models.CharField('token', max_length=50L, blank=True)
    total = models.FloatField('消费总额', default=0)
    level = models.IntegerField('级别', default=0)
    class Meta:
        verbose_name_plural = '用户列表'
        verbose_name = '用户列表'
        db_table = 'xgxm_user'
    def __unicode__(self):
        return str(self.userid) + "-" + self.name

class XgxmColproduct(models.Model):
    user = models.ForeignKey(XgxmUser)
    product = models.ForeignKey(XgxmProduct)
    class Meta:
        verbose_name_plural = '收藏产品'
        verbose_name = '收藏产品'
        db_table = 'xgxm_colproduct'
    def __unicode__(self):
        return str(self.user.userid)+'-'+str(self.product.productid)

class XgxmRecord(models.Model):
    recordid = models.AutoField('流水号', primary_key=True)
    otid = models.CharField('out_trade_no', max_length=50L)
    userid = models.IntegerField('用户号')
    productid = models.IntegerField('产品号')
    number = models.IntegerField('数量', default=0)
    total = models.FloatField('金额', default=0)
    detail = models.CharField('发货信息', max_length=500L)
    date = models.DateTimeField('日期', auto_now=True)
    status = models.IntegerField('订单状态', choices=((0, '已退款'), (1, '已入帐'), (2, '未付款'), (3, '已发货')))
    kdcom = models.CharField('快递公司', blank=True, max_length=50L)
    kdnu = models.CharField('快递单号', blank=True, max_length=50L)
    class Meta:
        verbose_name_plural = '订单记录'
        verbose_name = '订单记录'
        db_table = 'xgxm_record'
    def __unicode__(self):
        return str(self.recordid)+"-"+self.otid

class XgxmQa(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField('问题', max_length=500L, blank=True)
    answer = models.CharField('回答', max_length=1000L, blank=True)
    class Meta:
        verbose_name_plural = '常见问题'
        verbose_name = '常见问题'
        db_table = 'xgxm_qa'
    def __unicode__(self):
        return self.question

class XgxmMain(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=500L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', choices=((0, '开启图'), (1, '商城banner'), (2, '文章')), default=2)
    class Meta:
        verbose_name_plural = '图文设置'
        verbose_name = '图文设置'
        db_table = 'xgxm_main'
    def __unicode__(self):
        return str(self.id)+self.title
