#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/29 16:11
# @Author  : ChenJunlin
from time import strftime, gmtime


def collect():
    from django.core.cache import cache
    from apps.servers.remote import Remote
    import requests
    import json
    import math
    list = cache.get('iplist')
    if list:
        for i in range(len(list)):
            ip = list[i]
            info = cache.get(ip)
            id = info[0]
            username = info[1]
            password = info[2]
            urlid = str(id)
            url = 'http://127.0.0.1:8000/servers/%s/' %(urlid)
            headers = {'Content-Type': 'application/json'}
            try:
                r = Remote(host=ip, username=username, password=password)
                os = str((r.ssh("lsb_release -a|grep 'Description'"))[0].split('\t', 1)[1]).replace('\n','')
                cpu = str(r.ssh("cat /proc/cpuinfo | grep name")[0].split(': ', 1)[1]).replace('\n', '')
                c_use = r.ssh("vmstat 1 3|sed '1d'|sed '1d'|awk '{print $15}'")
                cpu_use = str(round((100 - (int(c_use[0]) + int(c_use[1]) + int(c_use[2])) / 3), 2)) + '%'
                hostname = str(r.ssh("hostname")[0]).replace('\n', '')
                sn = str(
                    r.ssh("dmidecode | grep 'Serial Number:' | grep -v Not | head -n 1 | awk  '{ print $3 }'")[0]).replace(
                    '\n', '')
                mem = str(math.ceil(int(
                    r.ssh("cat /proc/meminfo|grep MemTotal")[0].split(':', 1)[1].lstrip().split(' ', 1)[
                        0]) / 1024 ** 2)) + 'Gib'
                m_use = r.ssh("cat /proc/meminfo|sed -n '1,4p'|awk '{print $2}'")
                m_total = round(int(m_use[0]) / 1024)
                m_available = round(int(m_use[2]) / 1024)
                mem_use = str(round(((m_total - m_available) / m_total) * 100, 2)) + "%"
                uuid = str(r.ssh("dmidecode -t system | grep UUID")[0].split(':', 1)[1]).lstrip().replace(
                    '\n', '').lower()
                manufacturer = str(
                    r.ssh("dmidecode -t system | grep Manufacturer")[0].split(':', 1)[1]).lstrip().replace('\n', '')
                model_name = str(
                    r.ssh("dmidecode -t system | grep Product")[0].split(':', 1)[1]).lstrip().replace('\n', '')
                network_name = str(
                    r.ssh("lspci |grep -i 'eth'")[0].split(':', 2)[2].lstrip().replace('\n', ''))
                network_mac = str(
                    r.ssh("ip address show | grep link/ether")[0].split(' ', 6)[5].lstrip().replace('\n', '').replace(':',                                                                                                     '').lower())
                disk_name = str(
                    r.ssh("lsblk | sed -n '2p'")[0].split(' ', 1)[0].lstrip().replace('\n', ''))
                disk_size = str(
                    r.ssh("lsblk | sed -n '2p' | awk '{print $4}'")[0].lstrip().replace('\n', ''))
                last_check = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                data = {
                            "status":"在线",
                            "os":os,
                            "cpu":cpu,
                            "cpu_use":cpu_use,
                            "hostname":hostname,
                            "sn":sn,
                            "mem":mem,
                            "uuid":uuid,
                            "manufacturer":manufacturer,
                            "model_name":model_name,
                            "mem_use":mem_use,
                            "network_name":network_name,
                            "network_mac":network_mac,
                            "disk_name":disk_name,
                            "disk_size":disk_size,
                            "last_check":last_check
                }
                requests.patch(url, data = json.dumps(data), headers=headers)
            except Exception as e:
                last_check = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                data = {
                            "status": "离线",
                            "last_check": last_check
                }
                requests.patch(url, data=json.dumps(data), headers=headers)
        else:
            print("Empty-----")
