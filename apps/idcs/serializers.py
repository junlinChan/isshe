#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 11:02
# @Author  : ChenJunlin
from .models import Idcs
from rest_framework import serializers

class IdcSerializer(serializers.ModelSerializer):
    """
    Idc模型序列化
    """
    class Meta:
        model = Idcs
        fields = '__all__'