from _datetime import datetime

from django.db import models
from DjangoUeditor.models import UEditorField


# Create your models here.
class GoodsCategory(models.Model):
    """
    商品分类
    """
    CATEGORY_TYPE = ((1, u'一级类目'), (2, u'二级类目'), (3, u'三级类目'))

    name = models.CharField(verbose_name='类别名',
                            default='',
                            max_length=30,
                            help_text='类别名')
    code = models.CharField(verbose_name='类别code',
                            default='',
                            max_length=30,
                            help_text='类别code')
    desc = models.TextField(verbose_name='类别描述', default='', help_text='类别描述')
    # 目录树级别
    category_type = models.IntegerField(verbose_name='类目级别',
                                        choices=CATEGORY_TYPE,
                                        help_text='类目级别')
    # 设置models有一个指向自己的外键
    parent_category = models.ForeignKey('self',
                                        verbose_name='父级目录',
                                        on_delete=models.CASCADE,
                                        null=True,
                                        blank=True,
                                        help_text='父目录',
                                        related_name='sub_cat')
    is_tab = models.BooleanField(verbose_name='是否导航',
                                 default=False,
                                 help_text='是否导航项')
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品类别'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    category = models.ForeignKey(GoodsCategory,
                                 on_delete=models.CASCADE,
                                 related_name='brands',
                                 null=True,
                                 blank=True,
                                 verbose_name="商品类目")
    name = models.CharField(verbose_name="品牌名",
                            default="",
                            max_length=30,
                            help_text="品牌名")
    desc = models.TextField(verbose_name="品牌描述",
                            default="",
                            max_length=200,
                            help_text="品牌描述")
    image = models.ImageField(max_length=200, upload_to="brands/")
    add_time = models.DateTimeField(verbose_name="添加时间", default=datetime.now)

    class Meta:
        verbose_name = "宣传品牌"
        verbose_name_plural = verbose_name
        db_table = "goods_goodsbrand"

    def __str__(self):
        return self.name


class Goods(models.Model):
    """
    商品
    """
    category = models.ForeignKey(GoodsCategory,
                                 verbose_name='商品类别',
                                 on_delete=models.CASCADE)
    goods_sn = models.CharField(verbose_name='商品唯一货号',
                                max_length=50,
                                default='')
    name = models.CharField(verbose_name='商品名', max_length=100)
    sold_num = models.IntegerField(verbose_name='销量', default=0)
    fav_num = models.IntegerField(verbose_name='收藏数', default=0)
    goods_num = models.IntegerField(verbose_name='库存数', default=0)
    market_price = models.FloatField(verbose_name='市场价', default=0)
    shop_price = models.FloatField(verbose_name='本店价', default=0)
    goods_brief = models.TextField(verbose_name='商品简介', max_length=500)
    goods_desc = UEditorField(verbose_name='商品描述',
                              imagePath='goods/images/',
                              width=800,
                              height=600,
                              filePath='goods/files/',
                              default='')
    ship_free = models.BooleanField(verbose_name='是否承担运费', default=False)
    # 首页展示的封面图
    goods_front_image = models.ImageField(upload_to='goods/images/',
                                          null=True,
                                          blank=True,
                                          verbose_name='封面图')
    # 首页中展示新品
    is_new = models.BooleanField(verbose_name='是否为新品',
                                 default=False,
                                 help_text='是否新品')
    # 商品详情页的热卖商品
    is_hot = models.BooleanField(verbose_name='是否热销',
                                 default=False,
                                 help_text='是否熱銷')
    click_num = models.IntegerField(verbose_name='点击数', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = "商品"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class GoodsImage(models.Model):
    """
    商品轮播图:详情页面
    """
    goods = models.ForeignKey(Goods,
                              verbose_name='商品',
                              on_delete=models.CASCADE,
                              related_name='images')
    image = models.ImageField(upload_to='',
                              verbose_name='图片',
                              null=True,
                              blank=True)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '商品图片'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class Banner(models.Model):
    """
    首页轮播广告图
    """
    goods = models.ForeignKey(Goods,
                              verbose_name='商品',
                              on_delete=models.CASCADE)
    image = models.ImageField(upload_to='banner/', verbose_name='轮播图片')
    index = models.IntegerField(verbose_name='轮播顺序', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '首页轮播'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class IndexAd(models.Model):
    """
    首页商品广告
    """
    category = models.ForeignKey(GoodsCategory,
                                 verbose_name='商品类目',
                                 on_delete=models.CASCADE,
                                 related_name='category')
    goods = models.ForeignKey(Goods,
                              on_delete=models.CASCADE,
                              related_name='goods')

    class Meta:
        verbose_name = '分类广告'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.goods.name


class HotSearchWords(models.Model):
    """
    搜索栏下方的热搜词
    """
    keywords = models.CharField(verbose_name='热搜词', default='', max_length=20)
    index = models.IntegerField(verbose_name='排序', default=0)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)

    class Meta:
        verbose_name = '热搜排行'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.keywords
