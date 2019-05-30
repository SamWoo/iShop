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
from goods.views import GoodsListViewSet, CategoryViewSet, BannerViewSet, HotSearchViewSet
from users.views import SmsCodeViewSet, UserViewSet
from iShop.settings import MEDIA_ROOT

router = DefaultRouter()
# 配置goods的url
router.register(r'goods', GoodsListViewSet, base_name='goods')
# 配置category的url
router.register(r'categories', CategoryViewSet, base_name='categories')
# 配置banner的url
router.register(r'banners', BannerViewSet, base_name='banners')
# 配置hotsearch的url
router.register(r'hotsearchs', HotSearchViewSet, base_name='hotsearchs')
# 配置verify code的url
router.register(r'codes', SmsCodeViewSet, base_name='codes')
# 配置users register的url
router.register(r'users', UserViewSet, base_name='users')

urlpatterns = [
    # path('admin/', admin.site.urls),
    path(r'xadmin/', xadmin.site.urls),
    # 富文本编辑器url
    path(r'ueditor/', include('DjangoUeditor.urls')),
    # Router路由
    url(r'^', include(router.urls)),
    # drf文档urls
    url('docs', include_docs_urls(title='iShop')),
    url('api-auth/', include('rest_framework.urls')),
    # django自带的auth-token认证
    url('api-token-auth/', views.obtain_auth_token),
    # use jwt token
    # path('jwt-auth/',views.obtain_jwt_token),
    url('login/', obtain_jwt_token),
    # 文件
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
]
