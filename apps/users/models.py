from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """
    用户信息
    """
    GENDER_CHOICES = (
        ('male', u'男'),
        ('female', u'女')
    )
    name = models.CharField(verbose_name='姓名', max_length=30, null=True, blank=True)
    gender = models.CharField(verbose_name='性别', max_length=6, choices=GENDER_CHOICES, default='female')
    birthday = models.DateField(verbose_name='生日', null=True, blank=True)
    mobile = models.CharField(verbose_name='电话', max_length=11)
    email = models.EmailField(verbose_name='邮箱', max_length=50, null=True, blank=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
