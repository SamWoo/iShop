__author__ = 'sam'
import os
import sys

pwd = os.path.dirname(os.path.realpath(__file__))
sys.path.append('../')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'iShop.settings')

import django

if django.VERSION >= (1, 7):
    django.setup()

from db_tools.data.product_data import row_data
from goods.models import Goods, GoodsCategory, GoodsImage

for goods_detail in row_data:
    goods = Goods()
    goods.name = goods_detail['name']
    # 前端中是“￥232”，数据库中是float类型，所以要替换掉
    goods.market_price = float(int(goods_detail["market_price"].replace("￥", "").replace("元", "")))
    goods.shop_price = float(int(goods_detail['sale_price'].replace("￥", "").replace("元", "")))
    goods.goods_brief = goods_detail['desc'] if goods_detail['desc'] is not None else ''
    goods.goods_desc = goods_detail['goods_desc'] if goods_detail['goods_desc'] is not None else ''
    # 取第一张作为封面图
    goods.goods_front_image = goods_detail['images'][0] if goods_detail['images'] else ''
    # 取最后一个作为类型名
    category_name = goods_detail['categorys'][-1]
    # 取当前子类对应的GoodsCategory对象，filter没有匹配的会返回空数组，不会抛出异常
    category = GoodsCategory.objects.filter(name=category_name)
    if category:
        goods.category = category[0]
    goods.save()

    for goods_image in goods_detail['images']:
        goods_image_intance = GoodsImage()
        goods_image_intance.image = goods_image
        goods_image_intance.goods = goods
        goods_image_intance.save()
