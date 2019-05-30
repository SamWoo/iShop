from django.db import models

# Create your models here.

from django.contrib.auth import get_user_model
from goods.models import Goods
from datetime import datetime

User = get_user_model()


class UserFav(models.Model):
    """
    用户收藏操作
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,
                              verbose_name='商品',
                              on_delete=models.CASCADE)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收藏'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.user.name


class UserAddress(models.Model):
    """
    用户收货地址
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    provice = models.CharField(verbose_name='省份', max_length=100, default='')
    city = models.CharField(verbose_name='城市', max_length=100, default='')
    district = models.CharField(verbose_name='区域', max_length=100, default='')
    address = models.CharField(verbose_name='详细地址', max_length=100, default='')
    signer_name = models.CharField(verbose_name='签收人',
                                   max_length=100,
                                   default='')
    signer_mobile = models.CharField(verbose_name='电话',
                                     max_length=11,
                                     default='')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户收货地址'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.address


class UserLeavingMessag(models.Model):
    """
    用户留言
    """
    MESSAGE_TYPES = ((1, '留言'), (2, '投诉'), (3, '询问'), (4, '售后'), (5, '求购'))

    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    message_type = models.IntegerField(verbose_name='留言类型',
                                       choices=MESSAGE_TYPES,
                                       default=1)
    subject = models.CharField(verbose_name='主题', max_length=100, default='')
    message = models.TextField(verbose_name='留言内容',
                               default='',
                               help_text='留言内容')
    file = models.FileField(verbose_name='上传的文件',
                            upload_to='message/images/',
                            help_text='上传的文件')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '用户留言'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.subject
