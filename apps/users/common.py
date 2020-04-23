#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 23:41
# @Author  : ChenJunlin
from django.contrib.auth import get_user_model

User = get_user_model()

def get_user_obj(uid):
    try:
        return User.objects.get(pk=uid)
    except User.DoesNotExist:
        return None