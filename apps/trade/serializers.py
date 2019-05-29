from rest_framework import serializers
from trade.models import OrderGoods, OrderInfo, ShoppingCart


class OrderGoodsSerializer(serializers.ModelSerializer):
    """
    订单商品
    """

    class Meta:
        model = OrderGoods
        fields = ('goods', 'goods_nums')


class OrderInfoSerializer(serializers.ModelSerializer):
    """
    订单信息
    """
    goods = OrderGoodsSerializer(many=True)

    class Meta:
        model = OrderInfo
        fields = '__all__'


class ShoppingCartSerializer(serializers.ModelSerializer):
    """
    购物车
    """

    class Meta:
        model = ShoppingCart
        fields = '__all__'
