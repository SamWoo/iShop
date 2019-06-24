from rest_framework import serializers
from trade.models import OrderGoods, OrderInfo, ShoppingCart
from django.contrib.auth import get_user_model
from goods.models import Goods
from goods.serializers import GoodsSerializer
import time

User = get_user_model()


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单商品
    """
    goods = GoodsSerializer(many=True)

    class Meta:
        model = OrderGoods
        fields = ('goods', 'goods_nums')


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    订单信息
    """
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    """
    订单信息
    """
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    # 生成订单的时候这些不用post
    pay_status = serializers.CharField(read_only=True)
    trade_no = serializers.CharField(read_only=True)
    order_sn = serializers.CharField(read_only=True)
    pay_time = serializers.DateTimeField(read_only=True)

    # alipay_url = serializers.SerializerMethodField(read_only=True)

    def generate_order_sn(self):
        '当前时间+userid+随机数'
        from random import Random
        rand_ins = Random()
        return '{time_str}{user_id}{rand_str}'.format(
            time_str=strftime("%Y%m%d%H%M%S"),
            user_id=self.context['request'].user.id,
            rand_str=rand_ins.randint(10, 99))

    def validate(self, attrs):
        attrs['order_sn'] = self.generate_order_sn()
        return attrs

    class Meta:
        model = OrderInfo
        fields = '__all__'


class ShoppingCartDetailSerializer(serializers.ModelSerializer):
    """
    购物车商品详情信息
    """
    # 一个购物车对应一个商品
    goos = GoodsSerializer(many=True)

    class Meta:
        model = ShoppingCart
        fields = ['goods', 'nums']


class ShoppingCartSerializer(serializers.Serializer):
    """
    购物车
    """
    # 获取当前登录的用户
    user = serializers.HiddenField(default=serializers.CurrentUserDefault)
    nums = serializers.IntegerField(required=True,
                                    label='数量',
                                    min_value=1,
                                    error_messages={
                                        "min_value": "商品数量不能小于一",
                                        "required": "请选择购买数量",
                                    },
                                    help_text='商品數量')
    # 这里是继承Serializer，必须指定queryset对象，如果继承ModelSerializer则不需要指定
    # goods是一个外键，可以通过这方法获取goods object中所有的值
    goods = serializers.PrimaryKeyRelatedField(required=True,
                                               queryset=Goods.objects.all(),
                                               help_text='商品')

    # 继承的Serializer没有save功能，必须写一个create方法
    def create(self, validated_data):
        # validated_data是已经处理过的数据
        # 获取当前用户
        # view中:self.request.user；serizlizer中:self.context["request"].user
        user = self.context['request'].user
        nums = validated_data['nums']
        goods = validated_data['goods']

        existed = ShoppingCart.objects.filter(user=user, goods=goods)
        # 如果购物车中有记录，数量+1
        # 如果购物车车没有记录，就创建
        if existed:
            existed = existed[0]
            existed.nums += nums
            existed.save()
        else:
            existed = ShoppingCart.objects.create(**validated_data)
        return existed

    # 更新购物车商品数量
    def update(self, instance, validated_data):
        instance.nums = validated_data['nums']
        instance.save()
        return instance
