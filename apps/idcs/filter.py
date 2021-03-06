#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 11:00
# @Author  : ChenJunlin
import django_filters

from .models import Idcs
from django.db.models import Q

class IdcFilter(django_filters.rest_framework.FilterSet):
    """
    Idc过滤类
    """
    name = django_filters.CharFilter(method='search_idc')

    def search_idc(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(letter__icontains=value))

    class Meta:
        model = Idcs
        fields = ['name']
