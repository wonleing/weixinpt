# -*- coding: utf-8 -*-
from django.db import models

class NongxinPx(models.Model):
    pxid = models.CharField('培训代号', max_length=20L, primary_key=True)
    pxname = models.CharField('培训名称', max_length=100L, blank=True)
    pxtime = models.CharField('培训时间', max_length=50L, blank=True)
    description = models.CharField('内容介绍', max_length=2000L, blank=True)
    tip = models.CharField('温馨提示', max_length=2000L, blank=True)
    method = models.CharField('报名方式', choices=(('jzbm','集中报名'),('dlbm','独立报名')), max_length=20L, blank=True)
    upto = models.IntegerField('人数上限', default=1000)
    endtime = models.DateTimeField('截止时间', blank=True)
    link = models.CharField('日程链接', max_length=200L, blank=True)
    class Meta:
        verbose_name = '培训列表'
        verbose_name_plural = '培训列表'
        db_table = 'nongxin_px'
    def __unicode__(self):
        return self.pxid

class NongxinRecord(models.Model):
    id = models.AutoField('报名编号', primary_key=True)
    pxname = models.CharField('培训名称', max_length=100L)
    company = models.CharField('单位', max_length=20L)
    name = models.CharField('姓名', max_length=20L)
    gender = models.CharField('性别', max_length=20L)
    race = models.CharField('民族', max_length=20L, blank=True)
    department = models.CharField('部门/机构', max_length=20L, blank=True)
    position = models.CharField('职务', max_length=20L, blank=True)
    contact = models.CharField('联系人', max_length=20L, blank=True)
    phone = models.CharField('联系电话', max_length=20L, blank=True)
    arrival = models.CharField('到达方式', max_length=20L, blank=True)
    anumber = models.CharField('航班/车次', max_length=20L, blank=True)
    adate = models.CharField('到达日期', max_length=20L, blank=True)
    atime = models.CharField('到达时间', max_length=20L, blank=True)
    astation = models.CharField('到达站名', max_length=20L, blank=True)
    hotel = models.CharField('单住/合住', max_length=20L)
    comment = models.CharField('备注', max_length=200L, blank=True)
    status = models.IntegerField('审核状态', choices=((0,'未审核'),(1,'已审核'),(2,'不批准')), max_length=20L)
    class Meta:
        verbose_name = '报名记录'
        verbose_name_plural = '报名记录'
        db_table = 'nongxin_record'
    def __unicode__(self):
        return self.name
