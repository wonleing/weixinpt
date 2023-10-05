# -*- coding: utf-8 -*-
from django.db import models

class EbreathMember(models.Model):
    memberid = models.AutoField('代理编号', primary_key=True)
    name = models.CharField('姓名', max_length=50L, blank=True)
    pic = models.CharField('地区', max_length=200L, blank=True)
    phone = models.CharField('电话', max_length=20L, blank=True)
    detail = models.CharField('详细备注', max_length=5000L, blank=True)
    level = models.IntegerField('级别', default=0)
    class Meta:
        verbose_name_plural = '代理商'
        verbose_name = '代理商'
        db_table = 'ebreath_member'
    def __unicode__(self):
        return self.memberid

class EbreathProduct(models.Model):
    productid = models.AutoField('产品编号', primary_key=True)
    title = models.CharField('产品名称', max_length=50L)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('轮播图', max_length=2000L, blank=True)
    otherpic = models.CharField('详情图', max_length=2000L, blank=True)
    price = models.FloatField('价格', default=0)
    origprice = models.FloatField('原价', default=0)
    tag = models.CharField('标签', max_length=50L, blank=True)
    style = models.CharField('规格', max_length=50L, blank=True)
    onsale = models.IntegerField('商城在售', choices=((0, '否'), (1, '是')), default=0)
    number = models.IntegerField('库存量', default=0)
    class Meta:
        verbose_name_plural = '产品列表'
        verbose_name = '产品列表'
        db_table = 'ebreath_product'
    def __unicode__(self):
        return str(self.productid) + "-" + self.title

class EbreathUser(models.Model):
    userid = models.AutoField('用户编号', primary_key=True)
    wxid = models.CharField('微信ID', max_length=50L, blank=True)
    name = models.CharField('用户昵称', max_length=50L, blank=True)
    detail = models.CharField('用户描述', max_length=500L, blank=True)
    pic = models.CharField('头像地址', max_length=500L, blank=True)
    address = models.CharField('收货信息', max_length=500L, blank=True)
    token = models.CharField('token', max_length=50L, blank=True)
    total = models.FloatField('消费总额', default=0)
    balance = models.FloatField('余额', default=0)
    level = models.IntegerField('级别', default=0)
    class Meta:
        verbose_name_plural = '用户列表'
        verbose_name = '用户列表'
        db_table = 'ebreath_user'
    def __unicode__(self):
        return str(self.userid) + "-" + self.name

class EbreathPay(models.Model):
    otid = models.CharField('out_trade_no', primary_key=True, max_length=50L)
    userid = models.IntegerField('用户编号')
    memberid = models.IntegerField('推广编号', default=0)
    amount = models.FloatField('付款额', default=0)
    date = models.DateTimeField('日期', auto_now=True)
    class Meta:
        verbose_name_plural = '付款记录'
        verbose_name = '付款记录'
        db_table = 'ebreath_pay'
    def __unicode__(self):
        return str(self.userid)+"-"+str(self.amount)

class EbreathRecord(models.Model):
    recordid = models.AutoField('流水号', primary_key=True)
    userid = models.IntegerField('用户号')
    productid = models.IntegerField('产品号')
    number = models.IntegerField('数量', default=0)
    total = models.FloatField('总金额', default=0)
    province = models.CharField('省', max_length=50L)
    city = models.CharField('市', max_length=50L)
    county = models.CharField('县', max_length=50L)
    detail = models.CharField('住址', max_length=200L)
    recname = models.CharField('收货人', max_length=50L)
    rectel = models.CharField('收货电话', max_length=50L)
    date = models.DateTimeField('日期', auto_now=True)
    status = models.IntegerField('订单状态', choices=((1, '未发货'), (2, '已取消'), (3, '已发货')))
    kdcom = models.CharField('快递公司', choices=(('jiuye','九曳'), ('shunfeng','顺丰'), ('ziti', '自提'), ('xiangyao', '乡谣')), blank=True, max_length=50L)
    kdnu = models.CharField('快递单号', blank=True, max_length=50L)
    class Meta:
        verbose_name_plural = '订单记录'
        verbose_name = '订单记录'
        db_table = 'ebreath_record'
    def __unicode__(self):
        return str(self.recordid)

class EbreathQa(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField('问题', max_length=500L, blank=True)
    answer = models.CharField('回答', max_length=1000L, blank=True)
    class Meta:
        verbose_name_plural = '常见问题'
        verbose_name = '常见问题'
        db_table = 'ebreath_qa'
    def __unicode__(self):
        return self.question

class EbreathComment(models.Model):
    id = models.AutoField('评论编号', primary_key=True) 
    userid = models.IntegerField('用户号')
    productid = models.IntegerField('产品编号')
    name = models.CharField('用户昵称', max_length=50L, blank=True)
    pic = models.CharField('头像地址', max_length=500L, blank=True)
    detail = models.CharField('评论内容', max_length=2000L, blank=True)
    link = models.CharField('链接URL', max_length=500L, blank=True)
    isshow = models.IntegerField('类型', choices=((0, '隐藏'), (1, '显示')), default=0)
    class Meta:
        verbose_name_plural = '用户评论'
        verbose_name = '用户评论'
        db_table = 'ebreath_comment'
    def __unicode__(self):
        return self.name + str(self.id)

class EbreathSetting(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', choices=((0, '开启页'), (1, '商城Banner'), (2, '充值优惠'), (3, '返佣比率'), (4, '邮费设置')), default=0)
    class Meta:
        verbose_name_plural = '设置'
        verbose_name = '设置'
        db_table = 'ebreath_setting'
    def __unicode__(self):
        return self.title
