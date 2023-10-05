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
class DfthSource(models.Model):
    sourcename = models.CharField('原料名称', max_length=50L, blank=True)
    number = models.FloatField('库存量', default=0)
    type = models.CharField('单位', max_length=20L, blank=False)
    class Meta:
        verbose_name_plural = '原料库存'
        verbose_name = '原料库存'
        db_table = 'dfth_source'
    def __unicode__(self):
        return self.sourcename

class DfthProduct(models.Model):
    productname = models.CharField('库存名称', max_length=50L, blank=True)
    number = models.IntegerField('库存量', default=0)
    type = models.CharField('单位', max_length=20L, blank=False)
    class Meta:
        verbose_name_plural = '产品库存'
        verbose_name = '产品库存'
        db_table = 'dfth_product'
    def __unicode__(self):
        return self.productname

class DfthSupplyer(models.Model):
    supplyername = models.CharField('供应商名称', max_length=20L, blank=True)
    address = models.CharField('地址', max_length=50L, blank=True)
    phone = models.CharField('电话', max_length=50L, blank=True)
    class Meta:
        verbose_name_plural = '供应商'
        verbose_name = '供应商'
        db_table = 'dfth_supplyer'
    def __unicode__(self):
        return self.supplyername

class DfthCustomer(models.Model):
    customername = models.CharField('客户名称', max_length=50L, blank=True)
    type = models.CharField('客户类型', max_length=20L, blank=True)
    district = models.CharField('大区', max_length=20L, blank=True)
    location = models.CharField('地区', max_length=20L, blank=True)
    contact = models.CharField('联系人', max_length=20L, blank=True)
    phone = models.CharField('电话', max_length=50L, blank=True)
    address = models.CharField('地址', max_length=200L, blank=True)
    invoiceinfo = models.CharField('开票信息', max_length=200L, blank=True)
    class Meta:
        verbose_name_plural = '客户表'
        verbose_name = '客户表'
        db_table = 'dfth_customer'
    def __unicode__(self):
        return self.customername

class DfthEmployee(models.Model):
    employeename = models.CharField('员工姓名', max_length=50L, blank=True)
    position = models.CharField('职务', max_length=20L, blank=True)
    phone = models.CharField('电话', max_length=20L, blank=True)
    password = models.CharField('密码', max_length=50L, blank=True)
    auth = models.CharField('权限', max_length=20L, blank=True)
    class Meta:
        verbose_name_plural = '员工表'
        verbose_name = '员工表'
        db_table = 'dfth_employee'
    def __unicode__(self):
        return self.employeename

class DfthContract(models.Model):
    contractid = models.CharField('合同编号', max_length=50L, primary_key=True)
    customername = models.ForeignKey('DfthCustomer', verbose_name='客户名称', db_column='customername')
    summary = models.CharField('合同摘要', max_length=200L, blank=True)
    total = models.IntegerField('总金额', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    class Meta:
        verbose_name_plural = '合同列表'
        verbose_name = '合同列表'
        db_table = 'dfth_contract'
    def __unicode__(self):
        return self.contractid

class DfthPurchase(models.Model):
    id = models.AutoField('采购编号', primary_key=True)
    supplyername = models.ForeignKey('DfthSupplyer', verbose_name='供应商名称', db_column='supplyername')
    sourcename = models.ForeignKey('DfthSource', verbose_name='原料名称', db_column='sourcename')
    number = models.FloatField('数量', default=0)
    price = models.FloatField('单价', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    keepdate = models.CharField('生产日期', max_length=50L, blank=True)
    location = models.CharField('产地', max_length=50L, blank=True)
    class Meta:
        verbose_name_plural = '采购记录'
        verbose_name = '采购记录'
        db_table = 'dfth_purchase'
    def __unicode__(self):
        return str(self.id)

class DfthConsume(models.Model):
    id = models.AutoField('领用流水号', primary_key=True)
    employeename = models.ForeignKey('DfthEmployee', verbose_name='员工名称', db_column='employeename')
    sourcename = models.ForeignKey('DfthSource', verbose_name='原料名称', db_column='sourcename')
    number = models.FloatField('数量', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    class Meta:
        verbose_name_plural = '原料领用'
        verbose_name = '原料领用'
        db_table = 'dfth_consume'
    def __unicode__(self):
        return str(self.id)

class DfthProduce(models.Model):
    id = models.AutoField('产出流水号', primary_key=True)
    productname = models.ForeignKey('DfthProduct', verbose_name='产品名称', db_column='productname')
    number = models.IntegerField('数量', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    keepdate = models.CharField('保质期至', max_length=50L, blank=True)
    class Meta:
        verbose_name_plural = '产出记录'
        verbose_name = '产出记录'
        db_table = 'dfth_produce'
    def __unicode__(self):
        return str(self.id)

class DfthSale(models.Model):
    id = models.AutoField('出货流水号', primary_key=True)
    productname = models.ForeignKey('DfthProduct', verbose_name='产品名称', db_column='productname')
    customername = models.ForeignKey('DfthCustomer', verbose_name='客户名称', db_column='customername')
    contractid = models.ForeignKey('DfthContract', verbose_name='合同编号', db_column='contractid')
    number = models.IntegerField('数量', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    keepdate = models.CharField('保质期至', max_length=50L, blank=True)
    price = models.FloatField('单价', default=0)
    invoice = models.CharField('已开发票号', max_length=50L, blank=True)
    class Meta:
        verbose_name_plural = '销售记录'
        verbose_name = '销售记录'
        db_table = 'dfth_sale'
    def __unicode__(self):
        return str(self.id)

class DfthIncome(models.Model):
    id = models.AutoField('收入流水号', primary_key=True)
    customername = models.ForeignKey('DfthCustomer', verbose_name='客户名称', db_column='customername')
    contractid = models.ForeignKey('DfthContract', verbose_name='合同编号', db_column='contractid')
    number = models.IntegerField('收入金额', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    class Meta:
        verbose_name_plural = '收入记录'
        verbose_name = '收入记录'
        db_table = 'dfth_income'
    def __unicode__(self):
        return str(self.id)

class DfthExpense(models.Model):
    id = models.AutoField('支出流水号', primary_key=True)
    username = models.CharField('申请人', max_length=50L, blank=True)
    type = models.CharField('支出类型', max_length=50L, choices=(('gz','工资'),('clf','差旅费'),('kq','客情'),('scxg','生产相关'),('bgfy','办公费用'),('cf','餐费'),('ygcf','员工餐费'),('fz','房租'),('ygflf','员工福利费'),('ygpxf','员工培训费'),('yf','运费'),('ggxcf','广告宣传费'),('jtf','交通费'),('yjf','邮寄费'),('fwf','服务费'),('sdf','水电费'),('gdfh','股东分红'),('ryf','燃油费'),('tcf','停车费'),('qcxlf','汽车修理费'),('qcbxf','汽车保险费'),('nzjj','年终奖金'),('dfylk','垫付原料款'),('qtzc','其它支出')))
    reason = models.CharField('原由备注', max_length=50L, blank=True)
    number = models.FloatField('金额', default=0)
    date = models.DateTimeField('日期', auto_now_add=True)
    status = models.IntegerField('审批状态', default=0, choices=((0,'未审核'),(1,'已审核'),(2,'已驳回'),(3,'已打款')))
    class Meta:
        verbose_name_plural = '支出记录'
        verbose_name = '支出记录'
        db_table = 'dfth_expense'
    def __unicode__(self):
        return str(self.id)

class DfthNotice(models.Model):
    text = models.CharField('公告内容', max_length=500L, blank=True)
    date = models.DateTimeField('修改时间', auto_now_add=True)
    status = models.IntegerField('显示状态', default=1, choices=((0,'不显示'),(1,'显示')))
    class Meta:
        verbose_name_plural = '公告板'
        verbose_name = '公告板'
        db_table = 'dfth_notice'
    def __unicode__(self):
        return self.text

class DfthDevice(models.Model):
    deviceid = models.CharField('设备编号', max_length=50L, primary_key=True)
    devicename = models.CharField('设备名称', max_length=50L)
    buydate = models.CharField('购买时间', max_length=50L, blank=True)
    price = models.IntegerField('价格', default=0)
    class Meta:
        verbose_name_plural = '设备列表'
        verbose_name = '设备列表'
        db_table = 'dfth_device'
    def __unicode__(self):
        return self.devicename
