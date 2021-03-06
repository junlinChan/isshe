#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 11:19
# @Author  : ChenJunlin
from .models import Cabinet
from rest_framework import serializers

class CabinetSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        idc_obj = instance.idc
        ret = super(CabinetSerializer, self).to_representation(instance)
        ret["idc"] = {
            "name": idc_obj.name,
            "id": idc_obj.id
        }
        return ret

    class Meta:
        model = Cabinet
        fields = '__all__'