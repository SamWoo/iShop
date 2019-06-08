#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author ：Sam
# @File : adminx.py
# @Software : PyCharm
import xadmin
from goods.models import GoodsImage, Goods, GoodsCategory, HotSearchWords, IndexAd, Banner, GoodsCategoryBrand


class GoodsAdmin(object):
    # 显示的列
    list_display = ['name', 'click_num', 'sold_num', 'fav_num', 'goods_num', 'market_price',
                    'shop_price', 'goods_brief', 'goods_desc', 'is_new', 'is_hot', 'add_time']
    # 可搜索的字段
    search_fields = ['name', 'shop_price']
    # 列表页可以直接编辑的
    list_editable = ['is_hot']
    # 过滤器
    list_filter = ["name", "click_num", "sold_num", "fav_num", "goods_num", "market_price",
                   "shop_price", "is_new", "is_hot", "add_time", "category__name"]
    # 富文本编辑器
    style_fields = {'goods_desc': 'ueditor'}

    # 在添加商品的时候可以添加商品图片
    class GoodsImagesInline(object):
        model = GoodsImage
        exclude = ['add_time']
        extra = 1
        style = 'tab'

    inlines = [GoodsImagesInline, ]


class GoodsCategoryAdmin(object):
    list_display = ['name', 'category_type', 'parent_category', 'add_time']
    list_filter = ["category_type", "parent_category", "name"]
    search_fields = ['name', ]


class BannerAdmin(object):
    list_display = ["goods", "image", "index"]


class IndexAdAdmin(object):
    list_display = ["category", "goods"]


class HotSearchAdmin(object):
    list_display = ["keywords", "index", "add_time"]


xadmin.site.register(Goods, GoodsAdmin)
xadmin.site.register(GoodsCategory, GoodsCategoryAdmin)
xadmin.site.register(HotSearchWords, HotSearchAdmin)
xadmin.site.register(IndexAd, IndexAdAdmin)
xadmin.site.register(Banner, BannerAdmin)
