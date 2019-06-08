#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author ：Sam
# @File : serializers.py
# @Software : PyCharm
from rest_framework import serializers

from goods.models import Goods, GoodsCategory, GoodsImage, Banner, HotSearchWords, GoodsCategoryBrand, IndexAd


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
    # 覆盖外键字段
    category = CategorySerializer()
    # images是数据库中设置的related_name="images"，把轮播图嵌套进来
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


class IndexCategorySerializer(serializers.ModelSerializer):
    # 某个大类商标，可以有多个商标，一对多的关系
    brands = BrandSerializer(many=True)
    # good有一个外键category，但这个外键指向的是三级类，直接反向通过外键category（三级类），取某个大类下面的商品是取不出来的
    goods = serializers.SerializerMethodField()
    # 在parent_category字段中定义的related_name="sub_cat"
    # 取二级商品分类
    sub_cat = CategorySerializer2(many=True)
    # 广告商品
    ad_goods = serializers.SerializerMethodField()

    def get_ad_goods(self, obj):
        goods_json = {}
        ad_goods = IndexAd.objects.filter(category_id=obj.id)
        if ad_goods:
            # 取到这个商品Queryset[0]
            good_ins = ad_goods[0].goods
            goods_json = GoodsSerializer(good_ins, many=False, context={'request': self.context['request']}).data
        return goods_json

    # 获取商品
    def get_goods(self, obj):
        # 将这个商品相关父类子类等都可以进行匹配
        all_goods = Goods.objects.filter(Q(category_id=obj.id) | Q(category__parent_category_id=obj.id) | Q(
            category__parent_category__parent_category_id=obj.id))
        goods_serializer = GoodsSerializer(all_goods, many=True, context={'request': self.context['request']})
        return goods_serializer.data

    class Meta:
        model = GoodsCategory
        fields = '__all__'


class HotSearchSerializer(serializers.ModelSerializer):
    """
    热搜
    """

    class Meta:
        model = HotSearchWords
        fields = '__all__'
