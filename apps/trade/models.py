from django.db import models
from django.contrib.auth import get_user_model
from goods.models import Goods
from datetime import datetime

# Create your models here.

User = get_user_model()


class ShoppingCart(models.Model):
    """
    购物车
    """
    user = models.ForeignKey(User, verbose_name='用户', on_delete=models.CASCADE)
    goods = models.ForeignKey(Goods,
                              verbose_name='商品',
                              on_delete=models.CASCADE,
                              help_text='商品')
    nums = models.IntegerField(verbose_name='商品数量',
                               default=0,
                               help_text='商品數量')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '购物车'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'goods')

    def __str__(self):
        return '{0}:{1}'.format(self.goods.name, self.nums)


class OrderInfo(models.Model):
    """
    订单信息
    """
    ORDER_STATUS = (('TRADE_SUCCESS', '成功'), ('TRADE_CLOSE', '超时关闭'),
                    ('WAIT_BUYER_PAY', '交易创建'), ('TRADE_FINISHED',
                                                 '交易结束'), ('paying', '待支付'))

    PAY_TYPE = (('alipay', '支付宝'), ('wechat', '微信'))
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    # 订单号唯一
    order_sn = models.CharField(verbose_name='订单号',
                                max_length=30,
                                unique=True,
                                null=True,
                                blank=True,
                                help_text='订单号')
    nonce_str = models.CharField(verbose_name='随机加密串',
                                 max_length=50,
                                 null=True,
                                 blank=True,
                                 help_text='随机加密串')
    trade_no = models.CharField(verbose_name='交易号',
                                max_length=100,
                                unique=True,
                                null=True,
                                blank=True,
                                help_text='交易号')
    pay_status = models.CharField(verbose_name='订单状态',
                                  choices=ORDER_STATUS,
                                  default='paying',
                                  max_length=30,
                                  help_text='订单状态')
    pay_type = models.CharField(verbose_name='支付类型',
                                choices=PAY_TYPE,
                                default='alipay',
                                max_length=10,
                                help_text='支付类型')
    post_script = models.TextField(verbose_name='订单留言',
                                   max_length=200,
                                   help_text='订单留言')
    order_mount = models.FloatField(verbose_name='订单金额',
                                    default=0.0,
                                    help_text='訂單金額')
    pay_time = models.DateTimeField(verbose_name='支付时间',
                                    null=True,
                                    blank=True,
                                    help_text='支付時間')

    #  收货信息
    address = models.CharField(verbose_name='收货地址',
                               max_length=100,
                               default='',
                               help_text='收货地址')
    signer_name = models.CharField(verbose_name='签收人',
                                   max_length=20,
                                   default='',
                                   help_text='签收人')
    signer_mobile = models.CharField(verbose_name='联系电话',
                                     max_length=11,
                                     help_text='联系电话')

    add_time = models.DateTimeField(verbose_name='添加时间',
                                    default=datetime.now,
                                    help_text='添加時間')

    class Meta:
        verbose_name = '订单信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order_sn)


class OrderGoods(models.Model):
    """
    订单内的商品详情
    """
    order = models.ForeignKey(OrderInfo,
                              on_delete=models.CASCADE,
                              verbose_name='订单信息',
                              related_name='goods')
    goods = models.ForeignKey(Goods,
                              on_delete=models.CASCADE,
                              verbose_name='商品')
    goods_nums = models.IntegerField(verbose_name='商品数量', default=0)

    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '订单商品'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.order.order_sn)
