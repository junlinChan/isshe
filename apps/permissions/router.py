#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 14:27
# @Author  : ChenJunlin
from rest_framework.routers import DefaultRouter
from .views import PermissionsViewset, GroupPermissionsViewset


permission_router = DefaultRouter()
permission_router.register(r'permissions', PermissionsViewset, basename="permissions")
permission_router.register(r'grouppermissions', GroupPermissionsViewset, basename="grouppermissions")