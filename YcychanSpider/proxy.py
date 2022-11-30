# -*- coding: utf-8 -*-
# @Time    : 2022/11/18 23:01
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : proxy.py
# @Software: PyCharm
import datetime
import json
import time

import requests


#  自定义ip代理池错误
class ProxyPoolError(Exception):
    pass


class ProxyIP:
    """代理IP类"""

    def __init__(self, ip, arg):
        self.host = ip  # 代理IP地址
        self.arg = arg  # 此IP的唯一标识
        self.date = int(time.time())  # 此代理的时间戳
        self.url = "http://%(user)s:%(password)s@%(server)s" % {
            "user": 'HABOYTN7',
            "password": '276DCC522A2A',
            "server": self.host,
        }  # 即将发出请求的URL地址
        self.keep_size = 0  # IP请求占用量

    def get_url(self):
        return self.url

    @staticmethod
    def get_proxy_ip():
        """在代理服务商获取代理IP"""
        url = 'https://proxy.qg.net/allocate?Key=%(key)s' % {'key': 'HABOYTN7'}
        resp = requests.get(url)  # 请求代理IP
        resp_json = json.loads(resp.text)  # json编码响应
        if resp_json['Code'] == 0:
            return {'host': resp_json['Data'][0]['host'], 'TaskID': resp_json['TaskID']}  # 返回获取到的IP数据
        else:
            raise ProxyPoolError(
                f'代理IP获取失败，请检查参数后重试\n 错误码：{resp_json["Code"]}\n 错误信息:{resp_json["Msg"]}')


class ProxyPool:
    """代理IP池"""

    def __init__(self, max_size: int):
        self.pool = []
        self.max_size = max_size
        self.length = 0

    def append(self, proxy_ip: ProxyIP):
        """末尾追加IP"""
        if len(self.pool) >= self.max_size:
            raise ProxyPoolError(
                '池子IP数量超过限制,请修改max_size规定大小后再插入IP\nIP Pool maximum quantity limit exceeded,Please reset max_size')
        self.pool.append(proxy_ip)
        self.length += 1

    def remove(self, index=-1, arg=''):
        """移除IP"""
        if index == -1:
            for i, ip in enumerate(self.pool):
                if ip.arg == arg:
                    del self.pool[i]
                    self.length -= 1
        else:
            del self.pool[index]
            self.length -= 1

    def get_proxy_ip(self):
        """提取池子中的IP"""
        if len(self.pool) <= 0:
            return 'NULL'
        for i, ip in enumerate(self.pool):
            now_date = int(time.time())
            if now_date - ip.date > 55:  # 单个代理IP使用不能超过55秒
                del self.pool[i]
                continue
            elif ip.keep_size < 20:  # 返回占用小于20的IP
                ip.keep_size += 1
                print(ip.keep_size)
                return ip
            else:
                return 'NULL'

    def release_proxy_ip(self, proxy_ip: ProxyIP):
        """释放池子中的IP"""
        for i, ip in enumerate(self.pool):
            if ip.arg == proxy_ip.arg:
                self.pool[i].keep_size -= 1
                print('当前池中IP数量为', self.length)
