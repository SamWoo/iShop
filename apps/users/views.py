from django.shortcuts import render
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from django.db.models import Q
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.response import Response
from rest_framework import status
from users.models import VerifyCode
from users.serializers import SmsSerializer, UserRegisterSerializer, UserDetailSerializer
from random import choice
from utils.yunpian import YunPian

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
        except Exception as e:
            return None


class SmsCodeViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    create:
        生成短信验证码
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


class UserViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin, viewsets.GenericViewSet):
    """
    create:
        创建用户
    retrieve:
        获取已登录用户信息
    update:
        更新用户信息
    """
    # serializer_class = UserRegisterSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)

        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict['token'] = jwt_encode_handler(payload)
        re_dict['name'] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict,
                        status=status.HTTP_201_CREATED,
                        headers=headers)

    #这里需要动态权限配置
    #1.用户注册的时候不应该有权限限制
    #2.当想获取用户详情信息的时候，必须登录才行
    def get_permissions(self):
        if self.action == 'retrieve':
            return [IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    #这里需要动态选择用哪个序列化方式
    #1.UserRegSerializer（用户注册），只返回username和mobile，会员中心页面需要显示更多字段，所以要创建一个UserDetailSerializer
    #2.问题又来了，如果注册的使用userdetailSerializer，又会导致验证失败，所以需要动态的使用serializer
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegisterSerializer
        return UserDetailSerializer

    #虽然继承了Retrieve可以获取用户详情，但是并不知道用户的id，所有要重写get_object方法
    #重写get_object方法，就知道是哪个用户了
    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
