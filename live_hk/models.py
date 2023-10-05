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

class LiveHkRecord(models.Model):
    name = models.CharField('姓名/wxid', max_length=200L)
    phone = models.CharField('电话/bid', max_length=20L)
    type = models.CharField('活动类型/eventid', max_length=20L)
    date = models.DateTimeField('更新日期', auto_now=True)
    class Meta:
        verbose_name_plural = '活动记录'
        verbose_name = '活动记录'
        db_table = 'live_hk_record'
    def __unicode__(self):
        return self.name

class LiveHkMain(models.Model):
    id = models.IntegerField('序号', primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', blank=False)
    class Meta:
        verbose_name_plural = '主索引'
        verbose_name = '主索引'
        db_table = 'live_hk_main'
    def __unicode__(self):
        return self.title

class LiveHkTopic(models.Model):
    id = models.IntegerField('话题编号', primary_key=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    score = models.IntegerField('得票数', default=0)
    class Meta:
        verbose_name_plural = '话题评选'
        verbose_name = '话题评选'
        db_table = 'live_hk_topic'
    def __unicode__(self):
        return self.description

class LiveHkMember(models.Model):
    wxid = models.CharField('微信ID', max_length=50L, blank=True)
    name = models.CharField('姓名', max_length=20L, blank=True)
    phone = models.CharField('联系电话', max_length=20L, blank=True)
    company = models.CharField('公司', max_length=50L, blank=True)
    job = models.CharField('职务', max_length=50L, blank=True)
    type = models.CharField('类型', max_length=50L, blank=True)
    point = models.IntegerField('积分', default=0)
    class Meta:
        verbose_name_plural = '会员信息'
        verbose_name = '会员信息'
        db_table = 'live_hk_member'
    def __unicode__(self):
        return self.name

class LiveHkAward(models.Model):
    bid = models.CharField('商家ID', max_length=50L, blank=True)
    type = models.CharField('活动代码或链接', max_length=500L, blank=False)
    pic = models.CharField('中奖图片', max_length=500L, blank=True)
    link = models.CharField('发奖链接', max_length=500L, blank=True)
    rate = models.IntegerField('几率', blank=False)
    point = models.IntegerField('奖励额', blank=False)
    amount = models.IntegerField('数量', default=0)
    class Meta:
        verbose_name_plural = '奖项设置'
        verbose_name = '奖项设置'
        db_table = 'live_hk_award'
    def __unicode__(self):
        return self.bid
