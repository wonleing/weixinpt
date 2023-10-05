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

class YukangyuanProduct(models.Model):
    productid = models.AutoField(primary_key=True)
    code = models.CharField('产品代码', max_length=50L, blank=True)
    name = models.CharField('产品名称', max_length=50L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    type = models.CharField('分类', max_length=20L, blank=False)
    brand = models.CharField('品牌', max_length=20L, blank=True)
    detail = models.CharField('详情URL', max_length=200L, blank=True)
    storage = models.IntegerField('库存', default=9999)
    flag = models.CharField('标识', max_length=20L, blank=False)
    price1 = models.IntegerField('一级价格', blank=False)
    price2 = models.IntegerField('二级价格', blank=False)
    price3 = models.IntegerField('门市价格', blank=False)
    class Meta:
        verbose_name_plural = '产品表'
        verbose_name = '产品表'
        db_table = 'yukangyuan_product'
    def __unicode__(self):
        return str(self.productid) + '-' + self.name

class YukangyuanSaler(models.Model):
    salerid = models.AutoField('业务员编号', primary_key=True)
    name = models.CharField('姓名', max_length=20L, blank=True)
    password = models.CharField('登录密码', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=50L, blank=True)
    class Meta:
        verbose_name_plural = '业务员表'
        verbose_name = '业务员表'
        db_table = 'yukangyuan_saler'
    def __unicode__(self):
        return str(self.salerid) + '-' + self.name

class YukangyuanCustomer(models.Model):
    customerid = models.CharField('客户编号', max_length=20L, primary_key=True)
    password = models.CharField('登录密码', max_length=50L, blank=True)
    name = models.CharField('名称', max_length=50L, blank=True)
    contact = models.CharField('联系人', max_length=10L, blank=True)
    phone = models.CharField('电话', max_length=20L, blank=True)
    address = models.CharField('地址', max_length=200L, blank=True)
    salerid = models.IntegerField('所属销售', default=0)
    privilege = models.CharField('权限', max_length=20L, blank=True)
    grade = models.IntegerField('等级', default=3)
    class Meta:
        verbose_name_plural = '客户表'
        verbose_name = '客户表'
        db_table = 'yukangyuan_customer'
    def __unicode__(self):
        return self.customerid + '-' + self.name

class YukangyuanOrder(models.Model):
    orderid = models.AutoField('订单编号', primary_key=True)
    customerid = models.CharField('客户编号', max_length=20L)
    date = models.DateTimeField('日期', auto_now_add=True)
    total = models.IntegerField('总金额', default=0)
    detail = models.CharField('详情', max_length=500L, blank=True)
    status = models.IntegerField('订单状态', choices=((1, '已下单'), (2, '已录入'), (3, '已结款')))
    class Meta:
        verbose_name_plural = '订单表'
        verbose_name = '订单表'
        db_table = 'yukangyuan_order'
    def __unicode__(self):
        return str(self.orderid)

class YukangyuanOrderdetail(models.Model):
    detailid = models.AutoField('详情流水号', primary_key=True)
    orderid = models.IntegerField('订单编号', default=0)
    customerid = models.CharField('客户编号', max_length=20L)
    productid = models.IntegerField('商品编号', blank=False)
    amount = models.IntegerField('数量', default=0)
    total = models.IntegerField('小计', default=0)
    status = models.IntegerField('状态', choices=((0, '未结单'), (1, '已结单')), default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    class Meta:
        verbose_name_plural = '订单明细'
        verbose_name = '订单明细'
        db_table = 'yukangyuan_orderdetail'
    def __unicode__(self):
        return str(self.orderid) + " - " + str(self.detailid)

class YukangyuanSupport(models.Model):
    supportid = models.AutoField('支持流水号', primary_key=True)
    customerid = models.CharField('客户编号', max_length=20L)
    reason = models.CharField('原由', max_length=50L, blank=True)
    detail = models.CharField('支持详情', max_length=200L, blank=True)
    total = models.IntegerField('总价值', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    class Meta:
        verbose_name_plural = '市场支持'
        verbose_name = '市场支持'
        db_table = 'yukangyuan_support'
    def __unicode__(self):
        return str(self.customerid) + " - " + self.reason

class YukangyuanReport(models.Model):
    reportid = models.AutoField('报告编号', primary_key=True)
    salerid = models.IntegerField('业务员编号', blank=False)
    content = models.CharField('报告详情', max_length=500L, blank=True)
    date = models.DateTimeField('日期', auto_now_add=True)
    class Meta:
        verbose_name_plural = '工作报告'
        verbose_name = '工作报告'
        db_table = 'yukangyuan_report'
    def __unicode__(self):
        return str(self.reportid) + " - " + str(self.salerid)

class YukangyuanReturn(models.Model):
    returnid = models.AutoField('退货流水号', primary_key=True)
    customerid = models.CharField('客户编号', max_length=20L)
    detail = models.CharField('退货明细', max_length=500L)
    reason = models.CharField('原由', max_length=50L, blank=True)
    total = models.IntegerField('总价值', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    class Meta:
        verbose_name_plural = '退货表'
        verbose_name = '退货表'
        db_table = 'yukangyuan_return'
    def __unicode__(self):
        return str(self.returnid) + " - " + str(self.customerid)
