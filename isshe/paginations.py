#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/1 22:32
# @Author  : ChenJunlin
from rest_framework.pagination import PageNumberPagination

#重写分页样式
class Pagination(PageNumberPagination):
    def get_page_size(self, request):
        try:
            page_size = int(request.query_params.get("page_size", -1))
            if page_size >= 0:
                return page_size
        except:
            pass
        return self.page_size