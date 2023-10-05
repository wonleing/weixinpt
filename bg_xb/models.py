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
                if BgXbMain.objects.get(id=dbtable.split("_")[-1]).type != 2:
                    verbose_name = '预留'
                    verbose_name_plural = '预留'
                else:
                    verbose_name = dbtable.split("_")[-1]+" - "+BgXbMain.objects.get(id=dbtable.split("_")[-1]).title
                    verbose_name_plural = dbtable.split("_")[-1]+" - "+BgXbMain.objects.get(id=dbtable.split("_")[-1]).title
            except:
                    verbose_name = '未填加'
                    verbose_name_plural = '未填加'
            db_table = dbtable
        def __unicode__(self):
            return self.title
    return MyClass

class BgXbMember(models.Model):
    memberid = models.CharField('公司代号', max_length=50L, primary_key=True)
    name = models.CharField('公司全称', max_length=50L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    otherpic = models.CharField('更多图片', max_length=2000L, blank=True)
    detail = models.CharField('详细介绍', max_length=5000L, blank=True)
    address = models.CharField('地址', max_length=500L, blank=True)
    lat = models.FloatField('纬度', blank=True)
    lon = models.FloatField('经度', blank=True)
    phone = models.CharField('电话', max_length=20L, blank=True)
    contact = models.CharField('联系人', max_length=20L, blank=True)
    level = models.IntegerField('优先级', default=0)
    class Meta:
        verbose_name_plural = '公司列表'
        verbose_name = '公司列表'
        db_table = 'bg_xb_member'
    def __unicode__(self):
        return self.memberid

class BgXbProduct(models.Model):
    productid = models.AutoField('产品编号', primary_key=True)
    member = models.ForeignKey(BgXbMember)
    level = models.IntegerField('优先级', default=0)
    type = models.IntegerField('分类', default=1)
    title = models.CharField('产品名称', max_length=50L)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    otherpic = models.CharField('更多图片', max_length=2000L, blank=True)
    price = models.FloatField('价格', default=0)
    tag = models.CharField('标签', max_length=50L, blank=True)
    onsale = models.IntegerField('商城在售', choices=((0, '否'), (1, '是')), default=0)
    class Meta:
        verbose_name_plural = '产品列表'
        verbose_name = '产品列表'
        db_table = 'bg_xb_product'
    def __unicode__(self):
        return str(self.productid) + "-" + self.title

class BgXbUser(models.Model):
    userid = models.AutoField('用户编号', primary_key=True)
    wxid = models.CharField('微信ID', max_length=50L, blank=True)
    name = models.CharField('用户昵称', max_length=50L, blank=True)
    detail = models.CharField('用户描述', max_length=500L, blank=True)
    pic = models.CharField('头像地址', max_length=500L, blank=True)
    address = models.CharField('收货信息', max_length=500L, blank=True)
    token = models.CharField('token', max_length=50L, blank=True)
    total = models.FloatField('消费总额', default=0)
    level = models.IntegerField('级别', default=0)
    class Meta:
        verbose_name_plural = '用户列表'
        verbose_name = '用户列表'
        db_table = 'bg_xb_user'
    def __unicode__(self):
        return str(self.userid) + "-" + self.name

class BgXbColmember(models.Model):
    user = models.ForeignKey(BgXbUser)
    member = models.ForeignKey(BgXbMember)
    class Meta:
        verbose_name_plural = '收藏公司'
        verbose_name = '收藏公司'
        db_table = 'bg_xb_colmember'
    def __unicode__(self):
        return str(self.user.userid)+'-'+str(self.member.memberid)

class BgXbColproduct(models.Model):
    user = models.ForeignKey(BgXbUser)
    product = models.ForeignKey(BgXbProduct)
    class Meta:
        verbose_name_plural = '收藏产品'
        verbose_name = '收藏产品'
        db_table = 'bg_xb_colproduct'
    def __unicode__(self):
        return str(self.user.userid)+'-'+str(self.product.productid)

class BgXbRecord(models.Model):
    recordid = models.AutoField('流水号', primary_key=True)
    otid = models.CharField('out_trade_no', max_length=50L)
    userid = models.IntegerField('用户号')
    productid = models.IntegerField('产品号')
    number = models.IntegerField('数量', default=0)
    total = models.FloatField('金额', default=0)
    detail = models.CharField('发货信息', max_length=500L)
    date = models.DateTimeField('日期', auto_now=True)
    status = models.IntegerField('订单状态', choices=((0, '已退款'), (1, '已入帐'), (2, '未付款'), (3, '已发货')))
    kdcom = models.CharField('快递公司', blank=True, max_length=50L)
    kdnu = models.CharField('快递单号', blank=True, max_length=50L)
    class Meta:
        verbose_name_plural = '订单记录'
        verbose_name = '订单记录'
        db_table = 'bg_xb_record'
    def __unicode__(self):
        return str(self.recordid)+"-"+self.otid

class BgXbQa(models.Model):
    id = models.IntegerField(primary_key=True)
    question = models.CharField('问题', max_length=500L, blank=True)
    answer = models.CharField('回答', max_length=1000L, blank=True)
    class Meta:
        verbose_name_plural = '常见问题'
        verbose_name = '常见问题'
        db_table = 'bg_xb_qa'
    def __unicode__(self):
        return self.question

class BgXbMain(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField('标题', max_length=50L, blank=True)
    description = models.CharField('描述', max_length=1000L, blank=True)
    pic = models.CharField('图片URL', max_length=200L, blank=True)
    link = models.CharField('链接URL', max_length=200L, blank=True)
    type = models.IntegerField('类型', choices=((0, '开启页'), (1, '商城Banner'), (2, '栏目')), default=2)
    class Meta:
        verbose_name_plural = '栏目索引'
        verbose_name = '栏目索引'
        db_table = 'bg_xb_main'
    def __unicode__(self):
        return self.title

#for r in BgXbMain.objects.filter(type=2):
#    globals()['BgXb'+str(r.id)] = getModel('bg_xb_'+str(r.id))
BgXb1 = getModel('bg_xb_1')
BgXb2 = getModel('bg_xb_2')
BgXb3 = getModel('bg_xb_3')
