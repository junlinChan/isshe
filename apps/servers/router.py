#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 15:24
# @Author  : ChenJunlin
from rest_framework.routers import DefaultRouter
from .views import ServerViewset, AddServerViewset, ServerCountViewset

servers_router = DefaultRouter()
servers_router.register(r'addserver', AddServerViewset, basename="addserver")
servers_router.register(r'servers', ServerViewset, basename="servers")
servers_router.register(r'ServerCount', ServerCountViewset, basename="ServerCount")