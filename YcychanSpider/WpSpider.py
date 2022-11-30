# -*- coding: utf-8 -*-
# @Time    : 2022/11/25 12:37
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : WpSpider.py
# @Software: PyCharm
import re


class WpSpider:
    @staticmethod
    def del_url_http(res):
        """删除链接中的http和https开头

        :return 切掉http后的源链接"""
        if type(res) == list:
            for index, url in enumerate(res):
                res[index] = re.sub(r'https*://', '', url)
        else:
            res = re.sub(r'https*://','',res)
        return res
