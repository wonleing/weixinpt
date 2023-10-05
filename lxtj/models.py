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

def getModel(dbtable):
    class MyClassMetaclass(models.base.ModelBase):
        def __new__(cls, name, bases, attrs):
            name += dbtable
            return models.base.ModelBase.__new__(cls, name, bases, attrs)
    class MyClass(models.Model):
        __metaclass__ = MyClassMetaclass
        id = models.IntegerField('视频ID', primary_key=True)
        cateid = models.IntegerField('分类ID', default=0)
        title = models.CharField('标题', max_length=50L, blank=True)
        description = models.CharField('描述', max_length=1000L, blank=True)
        pic = models.CharField('图片URL', max_length=200L, blank=True)
        tag = models.CharField('标签', max_length=200L, blank=True)
        suetime = models.CharField('上映时间', max_length=200L, blank=True)
        director = models.CharField('导演', max_length=200L, blank=True)
        actors = models.CharField('演员', max_length=200L, blank=True)
        focus = models.CharField('看点', max_length=200L, blank=True)
        score = models.CharField('评分', max_length=200L, blank=True)
        series = models.IntegerField('是否多集', default=0)
        update = models.IntegerField('总集数', default=0)
        link = models.CharField('链接URL', max_length=200L, blank=True)
        class Meta:
            if str(dbtable) == 'lxtj_free':
                verbose_name = '免费影片'
                verbose_name_plural = '免费影片'
            elif str(dbtable) == 'lxtj_lg':
                verbose_name = '付费影片'
                verbose_name_plural = '付费影片'
            db_table = dbtable
        def __unicode__(self):
            return self.title
    return MyClass

class LxtjMember(models.Model):
    sn = models.CharField('SN码', max_length=20L)
    wxid = models.CharField('微信ID', max_length=50L, blank=True)
    ip = models.CharField('盒子IP', max_length=20L, blank=True)
    point = models.IntegerField('积分', default=0)
    class Meta:
        verbose_name_plural = '绑定信息'
        verbose_name = '绑定信息'
        db_table = 'lxtj_member'
    def __unicode__(self):
        return "%06d" %self.id + " - " + self.sn

class LxtjPayment(models.Model):
    sn = models.CharField('设备码', max_length=50L)
    cpid = models.CharField('CPID', max_length=20L)
    fee = models.IntegerField('付费', default=0)
    date = models.DateTimeField('购买日期', auto_now=True)
    class Meta:
        verbose_name_plural = '付费信息'
        verbose_name = '付费信息'
        db_table = 'lxtj_payment'
    def __unicode__(self):
        return self.sn + " - " + self.cpid

class LxtjMain(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    class Meta:
        verbose_name_plural = '免费专区'
        verbose_name = '免费专区'
        db_table = 'lxtj_main'
    def __unicode__(self):
        return self.title

class LxtjCharge(models.Model):
    operationid = models.CharField('运营ID', max_length=10L, primary_key=True)
    cpid = models.CharField('CPID', max_length=10L, blank=True)
    title = models.CharField('运营热词', max_length=50L, blank=True)
    price = models.IntegerField('折扣价', default=0, blank=False)
    origprice = models.IntegerField('原价', default=0, blank=False)
    active = models.IntegerField('是否启用', default=0, blank=False)
    class Meta:
        verbose_name_plural = '付费专区'
        verbose_name = '付费专区'
        db_table = 'lxtj_charge'
    def __unicode__(self):
        return self.title

#for r in LxtjMain.objects.all():
#    globals()['Lxtj'+str(r.id)] = getModel('lxtj_'+str(r.id))

globals()['LxtjLg'] = getModel('lxtj_lg')
globals()['LxtjFree'] = getModel('lxtj_free')
