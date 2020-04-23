#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 17:03
# @Author  : ChenJunlin
from rest_framework.routers import DefaultRouter
from .views import HardwareViewset

hadware_router = DefaultRouter()
hadware_router.register(r'hardware', HardwareViewset, basename="hardware")