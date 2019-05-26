#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author ：Sam
# @File : serializers.py
# @Software : PyCharm
from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, HotSearchWords, GoodsCategoryBrand


class CategorySerializer3(serializers.ModelSerializer):
    """
    三级目录
    """

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer2(serializers.ModelSerializer):
    """
    二级目录
    """
    sub_cat = CategorySerializer3(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    """
    一级目录
    """
    sub_cat = CategorySerializer2(many=True)

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class GoodsImagesSerializer(serializers.ModelSerializer):
    """
    商品轮播图
    """

    class Meta:
        model = GoodsImage
        fields = ('image',)


class GoodsSerializer(serializers.ModelSerializer):
    """
    商品列表页
    """
    category = CategorySerializer()
    images = GoodsImagesSerializer(many=True)

    class Meta:
        model = Goods
        # 全字段
        fields = '__all__'


class BannerSerializer(serializers.ModelSerializer):
    """
    首页轮播图
    """

    class Meta:
        model = Banner
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    """
    某个大类下的宣传商标
    """

    class Meta:
        model = GoodsCategoryBrand
        fields = '__all__'


class HotSearchSerializer(serializers.ModelSerializer):
    """
    热搜
    """

    class Meta:
        model = HotSearchWords
        fields = '__all__'
