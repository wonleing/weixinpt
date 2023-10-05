# -*- coding: utf-8 -*-
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#     * Rearrange models' order
#     * Make sure each model has one field with primary_key=True
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals
from django.db import models

class JysoftContract(models.Model):
    client = models.CharField('项目名称', max_length=50L, primary_key=True)
    amount = models.FloatField('数额', default=0)
    pname = models.CharField('客户名', max_length=20L, blank=True)
    contact = models.CharField('联系人', max_length=20L, blank=True)
    phone = models.CharField('联系电话', max_length=20L, blank=True)
    starttime = models.DateTimeField('录入日期', auto_now=True)
    nexttime = models.CharField('下次付费日期', max_length=20L, blank=True)
    seller = models.CharField('付款状态', max_length=20L, blank=True)
    class Meta:
        db_table = 'jysoft_contract'
        verbose_name_plural = '项目表'
        verbose_name = '项目表'
    def __unicode__(self):
        return self.client

class JysoftFinance(models.Model):
    type = models.IntegerField('收/支', choices=((0, '支出'), (1, '收入')))
    year = models.IntegerField('年', default=2017)
    month = models.IntegerField('月', default=0)
    day = models.IntegerField('日', default=0)
    summary = models.CharField('摘要', max_length=500L, blank=True)
    amount = models.FloatField('金额', default=0)
    user = models.CharField('经办人', max_length=50L, blank=True)
    message = models.CharField('备注', max_length=500L, blank=True)
    date = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        db_table = 'jysoft_finance'
        verbose_name_plural = '收支表'
        verbose_name = '收支表'
    def __unicode__(self):
        return self.summary

class JysoftMiaochun(models.Model):
    type = models.IntegerField('收/支', choices=((0, '支出'), (1, '收入')))
    year = models.IntegerField('年', default=2019)
    month = models.IntegerField('月', default=0)
    day = models.IntegerField('日', default=0)
    summary = models.CharField('摘要', max_length=500L, blank=True)
    amount = models.FloatField('金额', default=0)
    user = models.CharField('经办人', max_length=50L, blank=True)
    message = models.CharField('备注', max_length=500L, blank=True)
    date = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        db_table = 'jysoft_miaochun'
        verbose_name_plural = '妙纯'
        verbose_name = '妙纯'
    def __unicode__(self):
        return self.summary
