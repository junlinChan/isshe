#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 22:10
# @Author  : ChenJunlin
from django.contrib.auth.models import Group

def get_group_obj(gid):
    try:
        return Group.objects.get(pk=gid)
    except Group.DoesNotExist:
        return None