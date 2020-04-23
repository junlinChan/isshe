#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 11:32
# @Author  : ChenJunlin
from rest_framework.routers import DefaultRouter
from .views import CabinetViewset


cabinet_router = DefaultRouter()
cabinet_router.register(r'cabinet', CabinetViewset, basename="cabinet")