from django.db import models
from datetime import datetime

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (('male', u'男'), ('female', u'女'))
    name = models.CharField(verbose_name='姓名',
                            max_length=30,
                            null=True,
                            blank=True,
                            help_text='姓名')
    gender = models.CharField(verbose_name='性别',
                              max_length=6,
                              choices=GENDER_CHOICES,
                              default='female',
                              help_text='性別')
    birthday = models.DateField(verbose_name='生日',
                                null=True,
                                blank=True,
                                help_text='生日')
    # 设置允许为空，因为前端只有一个值，是username，所以mobile可以为空
    mobile = models.CharField(verbose_name='电话',
                              max_length=11,
                              null=True,
                              blank=True,
                              help_text='電話')
    email = models.EmailField(verbose_name='邮箱',
                              max_length=50,
                              null=True,
                              blank=True,
                              help_text='郵箱')

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class VerifyCode(models.Model):
    """
    SMS验证码
    """
    mobile = models.CharField(verbose_name='手机号',
                              max_length=11,
                              default='',
                              help_text='手機號')
    code = models.CharField(verbose_name='验证码',
                            max_length=4,
                            default='',
                            help_text='驗證碼')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '验证码'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.code
