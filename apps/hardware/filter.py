#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 16:55
# @Author  : ChenJunlin
import django_filters

from .models import Hardware
from django.db.models import Q

class HardwareFilter(django_filters.rest_framework.FilterSet):
    """
    Idc过滤类
    """
    name = django_filters.CharFilter(method='search_hadware')

    def search_hadware(self, queryset, name, value):
        return queryset.filter(Q(name__icontains=value) | Q(manufacturer__icontains=value))

    class Meta:
        model = Hardware
        fields = ['name', 'manufacturer']