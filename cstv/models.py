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

class CstvVideos(models.Model):
    video_id = models.AutoField('视频ID', primary_key=True)
    title = models.CharField('标题', max_length=50L, default='测试视频')
    description = models.IntegerField('播放次数', default=0)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('视频URL', max_length=200L, blank=True)
    tag = models.CharField('分类', max_length=200L, default='默认')
    update = models.DateTimeField('添加时间', auto_now_add=True)
    update.editable = True
    class Meta:
        verbose_name = '视频列表'
        verbose_name_plural = '视频列表'
        db_table = 'cstv_videos'
    def __unicode__(self):
        return self.title

class CstvSettings(models.Model):
    key = models.CharField('选项', max_length=50L)
    value = models.CharField('值', max_length=500L, blank=True)
    class Meta:
        verbose_name_plural = '设置'
        verbose_name = '设置'
        db_table = 'cstv_settings'
    def __unicode__(self):
        return self.key + " - " + self.value
