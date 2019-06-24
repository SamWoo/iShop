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
    price_min = NumberFilter(field_name='shop_price',
                             help_text='最低价格',
                             lookup_expr='gte')
    price_max = NumberFilter(field_name='shop_price',
                             help_text='最高价格',
                             lookup_expr='lte')
    # 商品一级分类，传入一级分类的ID
    top_category = NumberFilter(field_name='category',
                                method='top_category_filter',
                                help_text='一級分類')

    def top_category_filter(self, queryset, name, value):
        # 不管当前点击的是一级分类二级分类还是三级分类，都能找到
        return queryset.filter(
            Q(category_id=value)
            | Q(category_parent_category_id=value)
            | Q(category_parent_category_parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['price_min', 'price_max', 'top_category', 'is_hot', 'is_new']
