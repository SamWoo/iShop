from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from user_operation.models import UserFav, UserAddress, UserLeavingMessag
from goods.serializers import GoodsSerializer

class UserFavDetailSerializer(serializers.ModelSerializer):
    goods=GoodsSerializer()

    class Meta:
        model=UserFav
        fields=['goods','id']

class UserFavSerializer(serializers.ModelSerializer):
    """
    用户收藏
    """
    #获取当前登录的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        #validate实现唯一联合，一个商品只能收藏一次
        validtors = [
            UniqueTogetherValidator(queryset=UserFav.objects.all(),
                                    fields=('user', 'goods'),
                                    message='已经收藏')
        ]
        model = UserFav
        # 收藏的时候需要返回商品的id，因为取消收藏的时候必须知道商品的id是多少
        fields = ['user', 'goods', 'id']
