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
                if TaobaoHxfMain.objects.get(id=dbtable.split("_")[-1]).type != 2:
                    verbose_name = '预留'
                    verbose_name_plural = '预留'
                else:
                    verbose_name = dbtable.split("_")[-1]+" - "+TaobaoHxfMain.objects.get(id=dbtable.split("_")[-1]).title
                    verbose_name_plural = dbtable.split("_")[-1]+" - "+TaobaoHxfMain.objects.get(id=dbtable.split("_")[-1]).title
            except:
                    verbose_name = '未填加'
                    verbose_name_plural = '未填加'
            db_table = dbtable
        def __unicode__(self):
            return self.title
    return MyClass

class TaobaoHxfMsg(models.Model):
    contact = models.CharField('昵称', max_length=200L, blank=True)
    content = models.CharField('留言', max_length=500L, blank=True)
    reply = models.CharField('回复', max_length=500L, blank=True)
    class Meta:
        verbose_name_plural = '留言板'
        db_table = 'taobao_hxf_msg'
    def __unicode__(self):
        return self.contact

class TaobaoHxfMain(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', blank=False)
    class Meta:
        verbose_name_plural = '主索引'
        db_table = 'taobao_hxf_main'
    def __unicode__(self):
        return self.title

TaobaoHxf1 = getModel('taobao_hxf_1')
TaobaoHxf2 = getModel('taobao_hxf_2')
TaobaoHxf3 = getModel('taobao_hxf_3')
TaobaoHxf4 = getModel('taobao_hxf_4')
TaobaoHxf5 = getModel('taobao_hxf_5')
TaobaoHxf6 = getModel('taobao_hxf_6')
TaobaoHxf7 = getModel('taobao_hxf_7')
