#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/5 16:41
# @Author  : ChenJunlin
from .models import Hardware
from rest_framework import serializers

class HardwareSerializer(serializers.ModelSerializer):
    """
    Hadware模型序列化
    """
    class Meta:
        model = Hardware
        fields = '__all__'