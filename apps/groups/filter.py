#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 22:10
# @Author  : ChenJunlin
import django_filters
from django.contrib.auth.models import Group

class GroupFilter(django_filters.rest_framework.FilterSet):
    """
    用户组过滤类
    """
    name = django_filters.CharFilter(field_name='name',lookup_expr='icontains')


    class Meta:
        model = Group
        fields = ['name']

