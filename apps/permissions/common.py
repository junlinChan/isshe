#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 14:27
# @Author  : ChenJunlin
from django.contrib.auth.models import Permission

def get_permission_obj(pid):
    try:
        return Permission.objects.get(pk=pid)
    except Permission.DoesNotExist:
        return None