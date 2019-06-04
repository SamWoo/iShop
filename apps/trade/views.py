from django.shortcuts import render
from rest_framework import mixins, viewsets
from trade.models import ShoppingCart, OrderGoods, OrderInfo
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from utils.permissions import IsOwnerOrReadOnly
from trade.serializers import ShoppingCartDetailSerializer, ShoppingCartSerializer, OrderDetailSerializer, OrderSerializer
from trade.models import ShoppingCart, OrderGoods, OrderInfo

# Create your views here.


class ShoppingCartViewSet(viewsets.ModelViewSet):
    """
    购物车功能
    list:
        获取购物车详情
    create：
        加入购物车
    delete：
        删除购物记录
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)
    serializer_class = ShoppingCartSerializer
    # 商品ID
    lookup_field = 'goods_id'

    # 库存数-1
    def perform_create(self, serializer):
        '创建购物车'
        shop_cart = serializer.save()
        goods = shop_cart.goods
        goods.goods_num -= shop_cart.nums
        goods.save()

    # 更新库存,修改可能是增加页可能是减少
    def perform_update(self, serializer):
        # 首先获取修改之前的库存数量
        existed_record = ShoppingCart.objects.get(id=serializer.instance.id)
        existed_nums = existed_record.nums
        # 先保存之前的数据existed_nums
        saved_record = serializer.save()
        # 变化的数量
        nums = saved_record.nums - existed_nums
        goods = existed_record.goods
        goods.goods_num -= nums
        goods.save()

    # 库存数+1
    def perform_destroy(self, instance):
        goods = instance.goods
        goods.goods_num += instance.nums
        goods.save()
        instance.delete()

    def get_serializer_class(self):
        if self.action == 'list':
            return ShoppingCartDetailSerializer
        return ShoppingCartSerializer

    # 获取购物车列表
    def get_queryset(self):
        return ShoppingCart.objects.fitler(user=self.request.user)


class OrderViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                   mixins.DestroyModelMixin, mixins.RetrieveModelMixin,
                   viewsets.GenericViewSet):
    """
    订单管理
    list:
        获取个人订单
    delete:
        删除订单
    create：
        新增订单
    retrieve:
        获取某个订单的详情
    """
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly)
    authentication_classes = (JSONWebTokenAuthentication,
                              SessionAuthentication)
    serializer_class = OrderSerializer

    def get_serializer_class(self):
        '动态获取serializer_class'
        if self.action == 'retrieve':
            return OrderDetailSerializer
        return OrderSerializer

    def get_queryset(self):
        '获取订单列表'
        return OrderInfo.objects.filter(user=self.request.user)

    # 在订单提交保存之前还需要多两步步骤，所以这里自定义perform_create方法
    # 1.将购物车中的商品保存到OrderGoods中
    # 2.清空购物车
    def perform_create(self, serializer):
        order = serializer.save()
        shop_carts = ShoppingCart.objects.filter(user=self.request.user)

        for shop_cart in shop_carts:
            order_goods = OrderGoods()
            order_goods.goods = shop_cart.goods
            order_goods.goods_nums = shop_cart.nums
            order_goods.order = order
            order_goods.save()

            shop_cart.delete()
        return order
