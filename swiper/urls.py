"""swiper URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from user import api as user_api
from social import api as social_api

urlpatterns = [
    url(r'^api/user/verify$', user_api.get_verify_code),  # 注册
    url(r'^api/user/login$', user_api.login),    # 登录
    url(r'^api/user/profile$', user_api.get_profile),      # 获取个人资料
    url(r'^api/user/profile/modify$', user_api.modify_profile),     # 修改个人资料
    url(r'^api/user/avatar/upload$', user_api.upload_avatar),   # 用户上传头像
    # social_api
    url(r'^api/social/users', social_api.get_users),       # 获取推荐列表
    url(r'^api/social/like', social_api.like),
    url(r'^api/social/superlike', social_api.superlike),
    url(r'^api/social/dislike', social_api.dislike),
    url(r'^api/social/rewind', social_api.rewind),       # 反悔
    url(r'^api/social/friends', social_api.friends),    # 查看好友列表

]
