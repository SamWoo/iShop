from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.response import Response
from rest_framework import status
from users.models import VerifyCode
from users.serializers import SmsSerializer,UserRegisterSerializer
from random import choice

User = get_user_model()


# Create your views here.
class CustomBackend(ModelBackend):
    """
    自定义用户认证
    """

    def authenticate(self, username=None, password=None, **kwargs):
        #用户名和手机都能登录
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password=password):
                return user
        except expression as identifier:
            return None


class SmsCodeViewSet(CreateModelMixin, GenericViewSet):
    """
    手机验证码
    """
    serializer_class = SmsSerializer

    def generate_code(self):
        """
        生成四位数字的验证码
        """
        seeds = '1234567890'
        code = ''.join([choice(seeds) for i in range(4)])
        return code

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        # 验证合法性
        serializer.is_valid(raise_exception=True)
        
        mobile = serializer.validated_data['mobile']
        yun_pian = YunPian(APIKEY)
        #生成验证码
        code = self.generate_code()
        sms_status = yun_pian.send_sms(code=code, mobile=mobile)

        if sms_status['code'] != 0:
            return Response({
                'mobile': sms_status["msg"],
            },
                            status=status.HTTP_400_BAD_REQUEST)
        else:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                'mobile': mobile,
            },
                            status=status.HTTP_201_CREATED)

class UserViewSet(CreateModelMixin,GenericViewSet):
    """
    用户注册
    """
    serializer_class=UserRegisterSerializer