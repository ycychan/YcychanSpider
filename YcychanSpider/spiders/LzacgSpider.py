# -*- coding: utf-8 -*-
# @Time    : 2022/11/6 14:37
# @Author  : dominoar
# @Email   : duominuoaier@gmail.com
# @File    : LzacgSpider.py
# @Software: PyCharm
import re

import settings
import scrapy
from scrapy.http import Response

from WpSpider import WpSpider
from YcychanSpider import header
from YcychanSpider.items import LzacgItem


class LzacgSpider(scrapy.Spider, WpSpider):
    name = "LzacgSpider"
    allowed_domains = ["lzacg.one"]
    home = 'https://lzacg.one/'

    # test
    # start_urls = ['https://lzacg.one/?s=%E6%81%8B%E7%88%B1']

    # 需要获取的资源链接全部返回给引擎进行获取
    def start_requests(self):
        # for i in range(34):
        for i in range(1, 34):  # 目标33页，需要+1
            lzacg_pc = LzacgItem()
            lzacg_pc['lz_type'] = 'PC'
            yield scrapy.http.Request(url=f'{self.home}galgame/page/{i}', headers=header.get_random_user_agents(),
                                      callback=self.resource_url_parse, meta={'item': lzacg_pc})

        for i in range(1, 15):  # 目标14页，需要+1
            yield scrapy.http.Request(url=f'{self.home}kr/page/{i}', headers=header.get_random_user_agents(),
                                      callback=self.resource_url_parse)

    def resource_url_parse(self, response: Response):
        """将每一页的每一个资源都返回给引擎"""
        try:
            lzacg = response.meta['item']  # 创建Item对象
        except KeyError:
            lzacg = LzacgItem()
            lzacg['lz_type'] = 'KrKr'
        posts = response.css('posts')
        for p in posts:
            lzacg['lz_author'] = self.get_res_author(p.css('.item-body > .item-tags'))
            res_url = p.css('.item-thumbnail a').re('<a.*?href="([\s\S]*?)"')[0]
            yield scrapy.http.Request(url=res_url, headers=header.get_random_user_agents(), meta={'item': lzacg})

    def parse(self, resp: Response, **kwargs):
        # 将鼠标停留在函数名上可以查看函数功能
        lzacg = resp.meta['item']
        lzacg['lz_title'] = self.get_res_title(resp)
        lzacg['lz_url'] = self.get_res_url(resp)
        lzacg['lz_images_urls'] = self.get_res_img_urls(resp)
        lzacg['lz_downlinks'] = self.get_res_downlinks(resp)
        lzacg['lz_contexts'] = self.get_res_contexts(resp)
        lzacg['lz_send_time'] = self.get_res_send_time(resp)
        lzacg['lz_other'] = '内容转载于量子ACG，侵权请联系管理员立即处理~~'
        yield lzacg

    @staticmethod
    def get_res_author(resp):
        try:
            res_author = resp.re('>(#[\s\S]*?)<')[0]
            res_author = re.sub('# ', '', res_author)
        except IndexError:
            res_author = 'EOR:1019'
        return res_author

    @staticmethod
    def get_res_title(resp):
        """获取资源标题"""
        try:
            res_title = resp.css('.article-title').re(r'<a.*?>([\s\S]*?)</a>')[0]
            return res_title
        except IndexError as e:
            return 'EOR:1000'

    @staticmethod
    def get_res_url(resp):
        """获取资源链接地址"""
        try:
            res_url = resp.css('.article-title').re(r'<a.*?href="([\s\S]*?)"')[0]
            return res_url
        except IndexError as e:
            return 'EOR:1002'

    @staticmethod
    def get_res_img_urls(resp):
        """获资源图片地址"""
        try:
            res_img_urls = resp.css('.wp-posts-content img').re(r'src="([\s\S]*?)"')
            # 留到以后如果目标服务器在wp-posts-content中插入了其他杂物图片的时候使用
            # res_img_urls = resp.css('.wp-block-image img').re(r'src="([\s\S]*?)"')
            # if len(res_img_urls) == 0:
            #     res_img_urls = resp.css('.wp-posts-content > p > a > img').re(r'src="([\s\S]*?)"')  # 第二种情况
            # elif len(res_img_urls == 0):
            #     res_img_urls = resp.css('.wp-posts-content > h4 > img').re(r'src="([\s\S]*?)"')  # 第三章情况
            return res_img_urls
        except IndexError as e:
            return 'EOR:1003'

    @staticmethod
    def get_res_downlinks(resp):
        """获取资源下载链接"""
        try:
            res_downlinks = resp.css('.wp-block-button__link').re(r'<a.*?href="([\s\S]*?)"')
            return res_downlinks
        except IndexError as e:
            return 'EOR:1004'

    @staticmethod
    def get_res_send_time(resp):
        """获取资源发布时间"""
        try:
            return re.sub(r'日|发布', '', re.sub(r'年|月', '-', resp.css('.meta-time').re('title="([\s\S]*?)"')[0]))
        except IndexError:
            return 'EOR:1006'

    @staticmethod
    def get_res_contexts(resp):
        """获取资源介绍内容"""
        try:
            try:
                wp_context = resp.css('.wp-posts-content').re(r'游戏介绍</h4>([\s\S]*?)<h4')[0]  # 第一种情况
            except IndexError:
                wp_context = resp.css('.wp-posts-content').re(r'游戏简介</h4>([\s\S]*?)<h4')[0]  # 第二种情况
            res_context = re.findall(r'([\s\S]*?)<br>|([\s\S]*?)</p>', wp_context)
            for index, context in enumerate(res_context):
                # 内容文字提纯（去除html标签）
                for text in context:
                    if text != '':
                        res_context[index] = re.sub(r'<p>|\n|</p>', '', text)
            # 剔除空值元祖上（方代码不会剔除空匹配元组）
            for index, context in enumerate(res_context):
                if type(context) == tuple:
                    res_context[index] = ''
            return res_context
        except IndexError as e:
            return 'EOR:1005'
