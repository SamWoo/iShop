#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author ：Sam
# @File : filters.py
# @Software : PyCharm
from django_filters.rest_framework import FilterSet
from django_filters import NumberFilter

from goods.models import Goods


class GoodsFilter(FilterSet):
    """
    商品过滤类
    """
    price_min = NumberFilter(field_name='shop_price', help_text='最低价格', lookup_expr='gte')
    price_max = NumberFilter(field_name='shop_price', help_text='最高价格', lookup_expr='lte')

    # top_category = NumberFilter(method='top_category_filter')

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max']
