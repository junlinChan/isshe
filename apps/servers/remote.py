#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Time    : 2020/3/2 16:24
# @Author  : ChenJunlin
import paramiko

class Remote(object):
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.port = port
        self.username = username
        self.password = password

    def ssh(self, cmd):
        self.cmd = cmd
        try:
            #对远程服务做判断，如果远程失败，返回False
            trans = paramiko.Transport((self.host, self.port))
            trans.connect(username=self.username, password=self.password)
        except Exception as e:
            print(e)
            return False
        else:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh._transport = trans
            stdin, stdout,stderr = ssh.exec_command(self.cmd)
            result = stdout.readlines()
            trans.close()
            return result
