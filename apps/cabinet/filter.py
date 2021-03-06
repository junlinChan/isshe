#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 11:18
# @Author  : ChenJunlin
import django_filters
from .models import Cabinet

class CabinetFilter(django_filters.rest_framework.FilterSet):
    """
    机柜过滤类
    """
    name = django_filters.CharFilter(lookup_expr="icontains")
    idc = django_filters.NumberFilter(method="search_idc")

    def search_idc(self, queryset, name, value):
        return queryset.filter(idc__pk=value)


    class Meta:
        model  = Cabinet
        fields = ['name', 'idc']