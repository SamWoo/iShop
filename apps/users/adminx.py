#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author ：Sam
# @File : adminx.py
# @Software : PyCharm
import xadmin
from xadmin import views
from .models import VerifyCode


class BaseSetting(object):
    # 添加主题功能
    enable_themes = True
    use_bootswatch = True


class GlobalSettings(object):
    # 全局配置，后台管理标题和页脚
    site_title = "iShop后台管理界面"
    site_footer = "SamBrother"
    # 菜单收缩
    # menu_style = "accordion"


class VerifyCodeAdmin(object):
    list_display = ['code', 'mobile', 'add_time']


xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSettings)
xadmin.site.register(VerifyCode, VerifyCodeAdmin)
