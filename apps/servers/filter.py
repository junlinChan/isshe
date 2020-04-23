#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 12:15
# @Author  : ChenJunlin
import django_filters
from django.db.models import Q

from .models import Server

class ServerFilter(django_filters.rest_framework.FilterSet):
    """
    服务器过滤类
    """

    hostname        = django_filters.CharFilter(method='search_server')
    idc             = django_filters.NumberFilter(method="search_idc")
    cabinet         = django_filters.NumberFilter(method="search_cabinet")

    def search_server(self, queryset, name, value):
        return queryset.filter(Q(hostname__icontains=value)|Q(ip__icontains=value))


    def search_idc(self, queryset, name, value):
        if value > 0:
            return queryset.filter(idc_id__exact=value)
        elif value == -1:
            return queryset.filter(idc_id__isnull=True)
        else:
            return queryset

    def search_cabinet(self, queryset, name, value):
        if value > 0:
            return queryset.filter(cabinet_id__exact=value)
        elif value == -1:
            return queryset.filter(cabinet_id__isnull=True)
        else:
            return queryset

    class Meta:
        model = Server
        fields = ['hostname', 'ip', 'idc', 'cabinet']