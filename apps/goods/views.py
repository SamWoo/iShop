from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend, filters
from rest_framework import mixins, generics, viewsets, filters
from rest_framework.pagination import PageNumberPagination

# Create your views here.
from goods.filters import GoodsFilter
from goods.models import Goods, GoodsCategory, HotSearchWords, Banner
from goods.serializers import GoodsSerializer, CategorySerializer, HotSearchSerializer, BannerSerializer


# 自定义分页功能
class GoodsPagination(PageNumberPagination):
    #默认每页显示的个数
    page_size = 12
    #页码参数,与起前端一致"page"
    page_query_param = 'page'
    #可以动态改变每页显示的个数
    page_size_query_param = 'page_size'
    #最多能显示多少页
    max_page_size = 100


# use mixin
# class GoodsList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     '商品列表页'
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

# use mixed-in
# class GoodsList(generics.ListAPIView):
#     """
#     商品列表页, 分页， 搜索， 过滤， 排序
#     """
#     queryset = Goods.objects.all()
#     serializer_class = GoodsSerializer
#     # 分页
#     pagination_class = GoodsPagination


# use viewsets & mixin
class GoodsListViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet):
    """
    list:
        商品列表，分页，搜索，过滤，排序
    retrieve:
        获取商品详情
    """
    queryset = Goods.objects.all()
    serializer_class = GoodsSerializer
    # 分页
    pagination_class = GoodsPagination
    # 过滤
    filter_backends = (DjangoFilterBackend, filters.SearchFilter,
                       filters.OrderingFilter)
    # 设置filter的类为我们自定义的类
    filter_class = GoodsFilter
    # 搜索功能
    search_fields = ('name', 'goods_brief', 'goods_desc')
    # 排序功能
    ordering_fields = ('sold_num', 'shop_price')


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                      viewsets.GenericViewSet):
    """
    list:
        商品分类列表数据
    retrieve:
        获取商品分类详情
    """
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer


class HotSearchViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        热搜词列表
    """
    queryset = HotSearchWords.objects.all().order_by('-index')
    serializer_class = HotSearchSerializer


class BannerViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        商品轮播图列表
    """
    queryset = Banner.objects.all().order_by('index')
    serializer_class = BannerSerializer


class IndexCategoryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    list:
        首页商品分类数据
    """
    queryset = GoodsCategory.objects.filter(is_tab=True,
                                            name__in=['生鲜食品', '酒水饮料'])
    # serializer_class = In
