# -*- coding: utf-8 -*-
# @Time    : 2022/11/16 17:00
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : main.py
# @Software: PyCharm
import time

import parsel
import requests
from scrapy.cmdline import execute

import header

execute('scrapy crawl LzacgSpider'.split())

# if __name__ == '__main__':
#     resp = requests.get(url='https://lzacg.one/2304', headers=header.get_random_user_agents())
#     text = parsel.Selector(resp.text)
#     img = text.css('.wp-posts-content > h4 > img').re('src="([\s\S]*?)"')
#     print(img)
