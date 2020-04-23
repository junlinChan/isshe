#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 23:21
# @Author  : ChenJunlin
from rest_framework.routers import DefaultRouter
from .views import GroupsViewset, UserGroupsViewset, GroupMembersViewset

group_router = DefaultRouter()
group_router.register(r'groups', GroupsViewset, basename="groups")
group_router.register(r'usergroups',UserGroupsViewset, basename="usergroups")
group_router.register(r'groupmembers', GroupMembersViewset, basename="groupmembers")
