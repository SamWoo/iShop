"""iShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.static import serve
from rest_framework.routers import DefaultRouter
from rest_framework.documentation import include_docs_urls
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token
import xadmin
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, HotSearchViewSet, IndexCategoryViewSet
from users.views import SmsCodeViewSet, UserViewSet
from user_operation.views import UserFavViewSet, UserAddressViewSet, UserLeavingMessageViewSet
from trade.views import ShoppingCartViewSet,OrderViewSet
from iShop.settings import MEDIA_ROOT

router = DefaultRouter()
# Goods
router.register(r'goods', GoodsListViewSet, base_name='goods')
# Category
router.register(r'categories', CategoryViewSet, base_name='categories')
# Banner
router.register(r'banners', BannerViewSet, base_name='banners')
# Hot Search Words
router.register(r'hotsearchs', HotSearchViewSet, base_name='hotsearchs')
# SMS Verfiy Code
router.register(r'codes', SmsCodeViewSet, base_name='codes')
# User Register
router.register(r'users', UserViewSet, base_name='users')
# User Favs
router.register(r'favs', UserFavViewSet, base_name='favs')
# User Address
router.register(r'addresses', UserAddressViewSet, base_name='addresses')
# User LeavingMessages
router.register(r'messages', UserLeavingMessageViewSet, base_name='messages')
# ShoppingCart
router.register(r'shopcarts', ShoppingCartViewSet, base_name='shopcarts')
# Orders
router.register(r'orders', OrderViewSet, base_name='orders')
# IndexGoods
router.register(r'indexgoods',IndexCategoryViewSet,base_name='indexgoods')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'xadmin/', xadmin.site.urls),
    # 富文本编辑器url
    path(r'ueditor/', include('DjangoUeditor.urls')),
    # Router路由
    url(r'^', include(router.urls)),
    # drf文档urls
    url('docs', include_docs_urls(title='iShop')),
    url('^api-auth/', include('rest_framework.urls')),
    # drf自带的auth-token认证
    url('^api-token-auth/', views.obtain_auth_token),
    # #jwt的认证接口
    url('^login/', obtain_jwt_token),
    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    # 第三方登录
    path('',include('social_django.urls',namespace='social')),
]
