# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import logging

import requests
import scrapy.downloadermiddlewares.httpproxy
from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

import proxy as Proxy


class YcychanspiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class YcychanspiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class ProxyMiddleware:
    """使用代理中间件"""
    proxy_pool: Proxy.ProxyPool  # IP池
    task_id_list: list  # 正在请求响应中的IP TaskID列表

    def __init__(self):
        self.proxy_pool = Proxy.ProxyPool(100)
        self.task_id_list = []
        self.task_proxy: Proxy.ProxyIP
        print('--------------------!!!!!!!!!!!!!!')

    def process_request(self, request: scrapy.http.Request, spider):
        proxy_ip = self.proxy_pool.get_proxy_ip()
        if proxy_ip == 'NULL':  # 代理池为空则去获取新的代理IP
            proxy_ip_data = Proxy.ProxyIP.get_proxy_ip()  # 获取代理IP
            task_id = proxy_ip_data['TaskID']
            ip = proxy_ip_data['host']
            proxy_ip = Proxy.ProxyIP(arg=task_id, ip=ip)  # 创建新的代理IP
            self.proxy_pool.append(proxy_ip)
            self.task_proxy = proxy_ip
            self.task_id_list.append(task_id)
            proxy_ip = self.proxy_pool.get_proxy_ip()
        request.meta.update({'proxy': proxy_ip.get_url()})

    def process_response(self, request, response, spider):
        self.proxy_pool.release_proxy_ip(self.task_proxy)  # 释放占用请求完成的IP
        for i, taskID in enumerate(self.task_id_list):  # 将完成的请求移除任务列表
            if self.task_proxy.arg == taskID:
                del self.task_id_list[i]
        return response