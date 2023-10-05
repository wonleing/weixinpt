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
        id = models.IntegerField(primary_key=True)
        title = models.CharField('标题', max_length=50L, blank=True)
        description = models.CharField('描述', max_length=1000L, blank=True)
        price = models.CharField('价格', max_length=20L, blank=True)
        pic = models.CharField('图片URL', max_length=200L, blank=True)
        link = models.CharField('链接URL', max_length=200L, blank=True)
        class Meta:
            try:
                if MygymMain.objects.get(id=dbtable.split("_")[-1]).type != 2:
                    verbose_name = '预留'
                    verbose_name_plural = '预留'
                else:
                    verbose_name = dbtable.split("_")[-1]+" - "+MygymMain.objects.get(id=dbtable.split("_")[-1]).title
                    verbose_name_plural = dbtable.split("_")[-1]+" - "+MygymMain.objects.get(id=dbtable.split("_")[-1]).title
            except:
                    verbose_name = '未填加'
                    verbose_name_plural = '未填加'
            db_table = dbtable
        def __unicode__(self):
            return self.title
    return MyClass

class MygymMain(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', blank=False)
    class Meta:
        verbose_name_plural = '主索引'
        verbose_name = '主索引'
        db_table = 'mygym_main'
    def __unicode__(self):
        return self.title

class MygymSite(models.Model):
    sid = models.CharField('中心编号', max_length=50L, primary_key=True)
    name = models.CharField('店名', max_length=50L, blank=True)
    location = models.CharField('地址', max_length=50L, blank=True)
    phone = models.CharField('电话', max_length=50L, blank=True)
    link = models.CharField('相册地址', max_length=200L, blank=True)
    password = models.CharField('密码', max_length=50L, blank=True)
    class Meta:
        verbose_name_plural = '中心信息'
        verbose_name = '中心信息'
        db_table = 'mygym_site'
    def __unicode__(self):
        return self.name

class MygymCustomer(models.Model):
    wxid = models.CharField('微信ID', max_length=200L, blank=True)
    cid = models.CharField('学号', max_length=50L, blank=True)
    name = models.CharField('姓名', max_length=50L, blank=True)
    phone = models.CharField('电话', max_length=50L)
    sid = models.CharField('中心编号', max_length=50L)
    class Meta:
        verbose_name_plural = '会员信息'
        verbose_name = '会员信息'
        db_table = 'mygym_customer'
    def __unicode__(self):
        return self.cid + " - " + self.name

Mygym1 = getModel('mygym_1')
Mygym2 = getModel('mygym_2')
Mygym3 = getModel('mygym_3')
