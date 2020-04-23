#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 11:11
# @Author  : ChenJunlin
from rest_framework.routers import DefaultRouter
from .views import IdcViewset


idc_router = DefaultRouter()
idc_router.register(r'idcs', IdcViewset, basename="idcs")