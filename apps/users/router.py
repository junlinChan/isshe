#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 23:52
# @Author  : ChenJunlin
from rest_framework.routers import DefaultRouter
from .views import UsersViewset, UserRegViewset, UserInfoViewset


user_router = DefaultRouter()
user_router.register(r'userreg', UserRegViewset, basename="userreg")
user_router.register(r'users', UsersViewset, basename="users")
user_router.register(r'userinfo', UserInfoViewset, basename="userinfo")