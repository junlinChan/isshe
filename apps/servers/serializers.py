#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 12:15
# @Author  : ChenJunlin
import math

from django.conf import settings

from rest_framework import serializers

from apps.servers.remote import Remote
from .models import Server
from raven.contrib.django.raven_compat.models import client
from django.core.cache import cache

class ServerSerializer(serializers.ModelSerializer):
    """
    服务器序列化类
    """
    last_check = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True, help_text="检查时间")

    def get_idc_name(self, idc_obj):
        try:
            return {
                "name": idc_obj.name,
                "id": idc_obj.id
            }
        except Exception as e:
            return {}

    def get_cabinet_name(self, cabinet_obj):
        try:
            return {
                "name": cabinet_obj.name,
                "id": cabinet_obj.id
            }
        except Exception as e:
            return {}

    def to_representation(self, instance):
        idc_name = self.get_idc_name(instance.idc)
        cabinet_name = self.get_cabinet_name(instance.cabinet)
        ret = super(ServerSerializer, self).to_representation(instance)
        ret["idc"] = idc_name
        ret["cabinet"] = cabinet_name
        return ret

    class Meta:
        model = Server
        exclude = ('username', 'password')

class AddServerSerializer(serializers.ModelSerializer):
    ip = serializers.CharField(max_length=32, label="IP", help_text="主机IP")
    username = serializers.CharField(max_length=32, label="主机用户名", help_text="主机登录用户名")
    password = serializers.CharField(style={"input_type": "password"}, label="密码", write_only=True, help_text="密码")
    server_type = serializers.CharField(max_length=32, label="主机类型", help_text="主机类型")
    use = serializers.CharField(max_length=35, label="用途", help_text="用途")

    def create(self, validated_data):
        ip = validated_data["ip"]
        username = validated_data["username"]
        password = validated_data["password"]
        r = Remote(host=ip, username=username, password=password)
        validated_data["os"] = str((r.ssh("lsb_release -a|grep 'Description'"))[0].split('\t', 1)[1]).replace('\n','')
        validated_data["cpu"] = str(r.ssh("cat /proc/cpuinfo | grep name")[0].split(': ', 1)[1]).replace('\n','')
        c_use = r.ssh("vmstat 1 3|sed '1d'|sed '1d'|awk '{print $15}'")
        validated_data["cpu_use"] = str(round((100 - (int(c_use[0]) + int(c_use[1]) + int(c_use[2])) / 3), 2)) + '%'
        m_use = r.ssh("cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'")
        m_total = round(int(m_use[0]) / 1024)
        m_available = round(int(m_use[2]) / 1024)
        validated_data["mem_use"] = str(round(((m_total - m_available) / m_total) * 100, 2)) + "%"
        validated_data["hostname"] = str(r.ssh("hostname")[0]).replace('\n','')
        validated_data["sn"] = str(r.ssh("dmidecode | grep 'Serial Number:' | grep -v Not | head -n 1 | awk  '{ print $3 }'")[0]).replace('\n', '')
        validated_data["mem"] = str(math.ceil(int(r.ssh("cat /proc/meminfo|grep MemTotal")[0].split(':', 1)[1].lstrip().split(' ', 1)[0])/1024**2)) + 'Gib'
        validated_data["uuid"] = str(r.ssh("dmidecode -t system | grep UUID")[0].split(':', 1)[1]).lstrip().replace('\n', '').lower()
        validated_data["manufacturer"] = str(r.ssh("dmidecode -t system | grep Manufacturer")[0].split(':', 1)[1]).lstrip().replace('\n', '')
        validated_data["model_name"] = str(r.ssh("dmidecode -t system | grep Product")[0].split(':', 1)[1]).lstrip().replace('\n', '')
        validated_data["network_name"] = str(r.ssh("lspci |grep -i 'eth'")[0].split(':', 2)[2].lstrip().replace('\n', ''))
        validated_data["network_mac"] = str(r.ssh("ip address show | grep link/ether")[0].split(' ', 6)[5].lstrip().replace('\n', '').replace(':', '').lower())
        validated_data["disk_name"] = str(r.ssh("lsblk | sed -n '2p'")[0].split(' ', 1)[0].lstrip().replace('\n', ''))
        validated_data["disk_size"] = str(r.ssh("lsblk | sed -n '2p' | awk '{print $4}'")[0].lstrip().replace('\n', ''))
        validated_data["status"] = "在线"
        instance = super(AddServerSerializer, self).create(validated_data=validated_data)
        instance.save()
        return instance

    class Meta:
        model = Server
        fields = ('id', 'ip', 'username', 'password', 'use', 'server_type', 'idc', 'cabinet')

class AutoReportSerializer(serializers.Serializer):
    """
    服务器信息自动上报接口序列化类
    """
    hostname = serializers.CharField(required=True, max_length=50, label="主机名", help_text="主机名")
    os = serializers.CharField(required=True, max_length=100, label="操作系统", help_text="操作系统")
    manufacturer = serializers.CharField(required=True, max_length=32, label="厂商名称", help_text="厂商名称")
    model_name = serializers.CharField(required=True, max_length=32, label="型号", help_text="型号")
    uuid = serializers.CharField(required=True, max_length=100, label="UUID", help_text="UUID")
    cpu = serializers.CharField(required=True, max_length=32, label="CPU", help_text="CPU")
    mem = serializers.CharField(required=True, max_length=100, label="内存", help_text="内存")
    disk = serializers.JSONField(required=True, label="磁盘", help_text="磁盘")
    #device = serializers.JSONField(required=True, label="网卡", help_text="网卡")
    sn = serializers.CharField(required=True, max_length=40, label="SN", help_text="SN")
    ip = serializers.IPAddressField(required=False, label="IP地址", help_text="IP地址")

    def get_server_obj(self, uuid):
        try:
            return Server.objects.get(uuid__exact=uuid)
        except Server.DoesNotExist:
            return None
        except Server.MultipleObjectsReturned:
            client.captureException()
            raise serializers.ValidationError("存在多条记录")

    def create_server(self, validated_data):
        server_obj = Server.objects.create(**validated_data)
        return server_obj

    def create(self, validated_data):
        uuid = validated_data["uuid"].lower()
        sn = validated_data["sn"].lower()
        try:
            if sn == uuid or sn.startswith("vmware"):
                server_obj = Server.objects.get(uuid__iexact=uuid)
            else:
                server_obj = Server.objects.get(sn__iexact=sn)
        except Server.DoesNotExist:
            return self.create_server(validated_data)
        else:
            return self.update_server(server_obj, validated_data)

    def update_server(self, server_obj, validated_data):
        # 更新
        server_obj.hostname = validated_data["hostname"]
        server_obj.os = validated_data["os"]
        server_obj.manufacturer = validated_data["manufacturer"]
        server_obj.model_name = validated_data["model_name"]
        server_obj.cpu = validated_data["cpu"]
        server_obj.mem = validated_data["mem"]
        server_obj.disk = validated_data["disk"]
        server_obj.save()
        return server_obj

    def to_representation(self, instance):
        ret = {
            "hostname": instance.hostname,
            "uuid": instance.uuid
        }
        return ret


