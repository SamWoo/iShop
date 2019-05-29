from rest_framework import serializers
import re
from iShop.settings import REGEX_MOBILE
from django.contrib.auth import get_user_model
from datetime import datetime, timedelta

User = get_user_model()


class SmsSerializer(serializers.ModelSerializer):
    """
    手机号序列化
    """
    mobile = serializers.CharField(max_length=11)

    #函数名必须：validate + 验证字段名
    def validate_mobile(self, mobile):
        """
        手机号码验证
        """
        # 是否已经注册
        if User.objects.filter(mobile=mobile).count():
            raise serializers.ValidationError('用户已存在')

        # 手机号是否合法
        if not re.match(REGEX_MOBILE, mobile):
            raise serializers.ValidationError('手机号码不合法')

        # 验证码发送频率
        # 60s内只能发送一次
        one_minutes_ago = datetime.now() - timedelta(
            hour=0, minutes=1, second=0)
        if VerifyCode.objects.filter(add_time__gt=one_minutes_ago,
                                     mobile=mobile):
            raise serializers.ValidationError('距上次发送验证码未超过60s')
        return mobile


