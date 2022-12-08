# -*- coding: utf-8 -*-
# @Time    : 2022/11/19 20:01
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : DmhySpider.py
# @Software: PyCharm
import logging
import traceback

import scrapy

# from header import get_random_user_agents
# import items


class DmhySpider(scrapy.Spider):
    name = "DmhySpider"
    allowed_domains = ["dmhy.anoneko.com"]
    home = 'https://dmhy.anoneko.com'

    # test
    start_urls = ['https://dmhy.anoneko.com/topics/list/page/5000']

    # def start_requests(self):
    #     """请求站点所有资源页面"""
    #     for i in range(1, 5000):
    #         url = f'https://dmhy.anoneko.com/topics/list/page/{i}'
    #         yield scrapy.http.Request(url=url, headers=get_random_user_agents(), callback=self.start_requests_parse)

    def start_requests_parse(self, resp: scrapy.http.Response):
        tr_list = resp.css('#topic_list > tbody > tr')  # 所有tr标签
        dmhy = items.DmhyItem()
        for tr in tr_list:
            try:
                td_list = tr.css('td')  # 获取所有tr中td标签
                dmhy['hy_send_time'] = self.get_res_send_time(td_list[0])  # 发布时间
                dmhy['hy_type'], dmhy['hy_type_url'] = self.get_res_type_data(td_list[1])
                dmhy['hy_title'], dmhy['hy_url'] = self.get_res_title_data(td_list[2])  # 标题
                dmhy['hy_author'], dmhy['hy_author_url'] = self.get_res_author_data(td_list[2])
                # 作者
                dmhy['hy_pikpak'], dmhy['hy_magnet'] = self.get_res_downlinks(td_list[3])  # 下载链接
                dmhy['hy_size'] = self.get_res_size(td_list[4])
                dmhy['hy_publisher'], dmhy['hy_publisher_url'] = self.get_res_publisher_data(td_list[-1])
                yield scrapy.http.Request(url=dmhy.get('hy_url'), meta={'item': dmhy})  # 返回每一个资源页的链接并转接item给parse
            except Exception as e:
                traceback.print_exc()

    def parse(self, resp: scrapy.http.Response, **kwargs):
        dmhy = resp.meta['item']

    def get_res_send_time(self, td):
        try:
            res_send_time = td.css('span').re('>([\s\S]*?)</span')[0]
        except IndexError:
            res_send_time = 'EOR:1009'
        return res_send_time

    def get_res_type_data(self, td):
        try:
            res_type = td.css('a font').re('>([\s\S]*?)</font')[0]
        except IndexError:
            res_type = 'EOR:1007'
        try:
            res_type_url = self.home + (td.css('a').re('href="([\s\S]*?)"')[0])
        except IndexError:
            res_type_url = 'EOR:1008'
        return res_type, res_type_url

    def get_res_title_data(self, td):
        try:
            res_url = self.home + (td.css('td > a').re('href="([\s\S]*?)"')[0])
        except IndexError:
            res_url = 'EOR:1010'
        try:
            res_title = td.css('td > a').re('>([\s\S]*?)</a>')[0]
        except IndexError:
            res_title = 'EOR:1011'
        return res_title, res_url

    def get_res_author_data(self, td):
        try:
            res_author = td.css('span > a').re('>([\s\S]*?)</a>')[0]
        except IndexError:
            res_author = 'EOR:1012'
        try:
            res_author_url = self.home + (td.css('span > a').re('href="([\s\S]*?)"')[0])
        except IndexError:
            res_author_url = 'EOR:1013'
        return res_author, res_author_url

    def get_res_downlinks(self, td):
        try:
            res_pikpak = td.css('.download-pikpak').re('href="([\s\S]*?)"')[0]
        except IndexError:
            res_pikpak = 'EOR:1014'
        try:
            res_magnet = td.css('.arrow-magnet').re('href="([\s\S]*?)"')[0]
        except IndexError:
            res_magnet = 'EOR:1015'
        return res_pikpak, res_magnet

    def get_res_size(self, td):
        try:
            res_size = td.re('>([\s\S]*?)</td')[0]
        except IndexError:
            res_size = 'EOR:1016'
        return res_size

    def get_res_publisher_data(self, td):
        try:
            res_publisher = td.css('td > a > span')
            if len(res_publisher) != 0:
                res_publisher = 'EOR:1017'
            else:
                res_publisher = td.css('td > a').re('>([\s\S]*?)</a>')[0]
        except IndexError:
            res_publisher = 'EOR:1017'
        try:
            res_publisher_url = self.home + (td.css('td>a').re('href="([\s\S]*?)"')[0])
        except IndexError:
            res_publisher_url = 'EOR:1018'
        return res_publisher, res_publisher_url
