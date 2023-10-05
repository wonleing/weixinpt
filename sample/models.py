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
                if __Pname__Main.objects.get(id=dbtable.split("_")[-1]).type != 2:
                    verbose_name = '预留'
                    verbose_name_plural = '预留'
                else:
                    verbose_name = dbtable.split("_")[-1]+" - "+__Pname__Main.objects.get(id=dbtable.split("_")[-1]).title
                    verbose_name_plural = dbtable.split("_")[-1]+" - "+__Pname__Main.objects.get(id=dbtable.split("_")[-1]).title
            except:
                    verbose_name = '未填加'
                    verbose_name_plural = '未填加'
            db_table = dbtable
        def __unicode__(self):
            return self.title
    return MyClass

class __Pname__Msg(models.Model):
    contact = models.CharField('昵称', max_length=200L, blank=True)
    content = models.CharField('留言', max_length=500L, blank=True)
    reply = models.CharField('回复', max_length=500L, blank=True)
    class Meta:
        verbose_name_plural = '留言板'
        db_table = '__pname___msg'
    def __unicode__(self):
        return self.contact

class __Pname__Main(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', blank=False)
    class Meta:
        verbose_name_plural = '主索引'
        db_table = '__pname___main'
    def __unicode__(self):
        return self.title

__Pname__1 = getModel('__pname___1')
__Pname__2 = getModel('__pname___2')
__Pname__3 = getModel('__pname___3')
__Pname__4 = getModel('__pname___4')
__Pname__5 = getModel('__pname___5')
__Pname__6 = getModel('__pname___6')
__Pname__7 = getModel('__pname___7')
