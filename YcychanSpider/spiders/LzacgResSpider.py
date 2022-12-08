# -*- coding: utf-8 -*-
# @Time    : 2022/12/3 16:33
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : LzacgResSpider.py
# @Software: PyCharm
import re

import parsel
import requests

# 请求头
headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,app\
          lication/signed-exchange;v=b3;q=0.9',
    'accept - encoding': 'gzip, deflate, br',
    'accept - language': 'zh - CN, zh;q = 0.9, en - US;q = 0.8, en;q = 0.7',
    'cache - control': 'no - cache',
    'cookie': '__cf_bm = 4RU8Upv_0td94cyCRQvgBvhxachIcmGQCP24Y_LTu04 - 1670078388 - 0 - AQDgCNN5udYi1OTTBj7Wmfv8nB9\
              rdVmxW3D1jOpwa + yBB4kVLGwX0RPBFNATG7y7NkSx2 / uOy7D5f4R1xJIcO8EL0tfC8Zhj + 9PNByBbdN6V3l1ddRmlok8vXknyoYR5\
              rcZqFXWVYv4gF9ZxtPI9wjU =;timezone = 8',
    'pragma': 'no - cache',
    'sec - ch - ua': '"Not?A_Brand";v = "8", "Chromium";v = "108", "Google Chrome";v = "108"',
    'sec - ch - ua - mobile': '?0',
    'sec - ch - ua - platform': '"Windows"',
    'sec - fetch - dest': 'document',
    'sec - fetch - mode': 'navigate',
    'sec - fetch - site': 'same - site',
    'sec - fetch - user': '?1',
    'upgrade - insecure - requests': '1',
    'user - agent': 'Mozilla / 5.0(WindowsNT10.0;Win64;x64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 108.0.0\
          .0Safari / 537.36'
}


def get_trs(text):
    """获取所有tr"""
    return text.css('#list-table tr')


def get_tr_res(text):
    return text.css('.file > a').re('href="([\s\S]*?)"')[0]


if __name__ == '__main__':
    # 请求页面
    resp = requests.get(url='https://oda.lzacg.one/', headers=headers)
    print('请求完成', resp, '开始解析……')
    # 解析资源列表
    html = parsel.Selector(resp.text)
    trs = get_trs(html)
    del trs[0]  # 清除杂项
    del trs[0]
    trs.pop()
    for index, tr in enumerate(trs):
        tr_url = get_tr_res(tr)
        print(tr_url)
