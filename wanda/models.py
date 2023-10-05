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

def getModel(dbtable, tname):
    class MyClassMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            name += dbtable
            return models.base.ModelBase.__new__(cls, name, bases, attrs)
    class MyClass(models.Model):
        __metaclass__ = MyClassMetaclass
        id = models.IntegerField(primary_key=True)
        title = models.CharField('标题', max_length=50L, blank=True)
        description = models.CharField('描述', max_length=1000L, blank=True)
        price = models.CharField('价格', max_length=20L, blank=True)
        pic = models.CharField('图片URL', max_length=200L, blank=True)
        link = models.CharField('链接URL', max_length=200L, blank=True)
        class Meta:
            verbose_name = tname
            verbose_name_plural = tname
            db_table = dbtable
        def __unicode__(self):
            return self.title
    return MyClass

class WandaEvent(models.Model):
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    amount = models.IntegerField('数量', blank=False)
    starttime = models.DateTimeField('开始时间', blank=False)
    class Meta:
        verbose_name_plural = '活动设置'
        verbose_name = '活动设置'
        db_table = 'wanda_event'
    def __unicode__(self):
        return self.title

class WandaAward(models.Model):
    level = models.IntegerField('等级', primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    rate = models.IntegerField('几率', blank=False)
    point = models.IntegerField('奖励', blank=False)
    amount = models.IntegerField('数量', default=0)
    class Meta:
        verbose_name_plural = '抽奖设置'
        verbose_name = '抽奖设置'
        db_table = 'wanda_award'
    def __unicode__(self):
        return self.title

class WandaRecord(models.Model):
    orderid = models.CharField('票号', max_length=100L, blank=True)
    wxid = models.CharField('购买ID', max_length=100L,  blank=True)
    shareid = models.CharField('分享ID', max_length=100L, blank=True)
    type = models.CharField('类型', max_length=50L)
    date = models.CharField('购买日期', max_length=50L, blank=True)
    class Meta:
        verbose_name_plural = '活动记录'
        verbose_name = '活动记录'
        db_table = 'wanda_record'
    def __unicode__(self):
        return self.type + self.orderid

class WandaMember(models.Model):
    wxid = models.CharField('微信ID', primary_key=True, max_length=50L)
    name = models.CharField('姓名', max_length=20L, blank=True)
    phone = models.CharField('联系电话', max_length=20L, blank=True)
    point = models.IntegerField('积分', default=0)
    description = models.CharField('描述', max_length=500L)
    address = models.CharField('地址', max_length=500L)
    class Meta:
        verbose_name_plural = '会员信息'
        verbose_name = '会员信息'
        db_table = 'wanda_member'
    def __unicode__(self):
        return self.name

class WandaPhoto(models.Model):
    wxid = models.CharField('微信ID', max_length=50L)
    piclink = models.CharField('图片URL', max_length=500L)
    date = models.DateTimeField('日期', auto_now=True)
    class Meta:
        verbose_name_plural = '照片上传'
        verbose_name = '照片上传'
        db_table = 'wanda_photo'
    def __unicode__(self):
        return self.wxid

class WandaMain(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', blank=False)
    class Meta:
        verbose_name_plural = '主索引'
        verbose_name = '主索引'
        db_table = 'wanda_main'
    def __unicode__(self):
        return self.title

Wanda1 = getModel('wanda_1', '1-推荐')
Wanda2 = getModel('wanda_2', '2-公开课')
Wanda3 = getModel('wanda_3', '3-精品店')
