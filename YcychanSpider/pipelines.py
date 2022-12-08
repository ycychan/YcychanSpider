# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import logging
from xml.dom import minidom

import pymysql
import xlwings as xlwings
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline

import YcychanSpider.items
from WpSpider import WpSpider

already_num = 0


# 管道存储数据默认此管道未使用
class YcychanspiderPipeline:
    def process_item(self, item, spider):
        return item


class LzacgSpiderPipeline:
    """存储量子ACG资源管道"""

    def __init__(self):
        # 连接到数据库
        self.db = self.db = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                            database='galgame')
        self.cursor = self.db.cursor()  # 数据库游标
        # 创建XML
        self.xml_doc = minidom.Document()
        self.xml_root = self.xml_doc.appendChild(self.xml_doc.createElement('Galgames'))  # 根节点
        self.fp = open('galgame.xml', 'w+', encoding='UTF-8')  # XML 文件保存位置

    def close_spider(self, spider):
        self.db.close()  # 关闭数据库链接
        self.xml_doc.writexml(self.fp, indent='\t', addindent='\t', newl='\n', encoding='UTF-8')  # 从内存写出XML至本地
        self.fp.close()  # 关闭xml文件流

    def process_item(self, item, spider):
        global already_num
        res_data = {}  # 资源列表
        res_data.update({'res_title': item.get('lz_title')})
        res_data.update({'res_url': item.get('lz_url')})
        res_data.update({'res_author': item.get('lz_author')})
        res_data.update({'res_type': item.get('lz_type')})
        res_data.update({'res_img_urls': item.get('lz_images_urls')})
        res_data.update({'res_downlinks': item.get('lz_downlinks')})
        res_data.update({'res_contexts': item.get('lz_contexts')})
        res_data.update({'res_send_time': item.get('lz_send_time')})
        res_data.update({'res_other': item.get('lz_other')})
        # 写出资源
        self.write_res(res_data)
        already_num += 1
        print("\r已完成爬取: {:d}".format(already_num), end='')

    def write_res(self, res_data):
        """将所有资源写出"""
        xml_galgames = self.xml_root.appendChild(self.xml_doc.createElement('Galgame'))
        for k in res_data:  # 将每一个kwargs元素遍历创建为节点
            xml_galgame_node = xml_galgames.appendChild(self.xml_doc.createElement(k))
            # 资源为列表的处理
            if type(res_data[k]) is list:
                # 资源链接处理
                if len(res_data[k]) != 0 and res_data[k][0].find('http') == -1:
                    for li in res_data[k]:  # 遍历文本内容
                        xml_galgame_node.appendChild(self.xml_doc.createTextNode(li))
                else:
                    for index in range(len(res_data[k])):  # 遍历http资源链接
                        if res_data[k][index] != '' and res_data[k][index].find('EOR') == -1:
                            res_url_node = xml_galgame_node.appendChild(self.xml_doc.createElement('url'))
                            res_url_node.appendChild(self.xml_doc.createTextNode(res_data[k][index]))
            else:
                if res_data[k] is not None and res_data[k].find('EOR') == -1:
                    xml_galgame_node.appendChild(self.xml_doc.createTextNode(res_data[k]))


class LzacgResourcePipeline(FilesPipeline):
    def get_media_requests(self, item, info):
        print(item.get('lz_type'))
        pass

    def file_path(self, request, response=None, info=None, *, item=None):
        pass


class DmhySpiderPipeline:
    def __init__(self):
        # 连接到数据库
        self.db = self.db = pymysql.connect(host='localhost', port=3306, user='root', password='root',
                                            database='dmhy_resource')
        self.cursor = self.db.cursor()  # 数据库游标
        # 创建XML
        self.xml_doc = minidom.Document()
        self.xml_root = self.xml_doc.appendChild(self.xml_doc.createElement('DmhyResource'))  # 根节点
        self.fp = open('DmhyResource.xml', 'w+', encoding='UTF-8')  # XML 文件保存位置

    def close_spider(self, spider):
        self.db.close()  # 关闭数据库链接
        self.xml_doc.writexml(self.fp, indent='\t', addindent='\t', newl='\n', encoding='UTF-8')  # 从内存写出XML至本地
        self.fp.close()  # 关闭xml文件流

    def process_item(self, item, spider):
        print('进入管道')
        res_data = {}  # 资源列表
        res_data.update({'res_title': item.get('hy_title')})
        res_data.update({'res_url': item.get('hy_url')})
        res_data.update({'res_pikpak': item.get('hy_pikpak')})
        res_data.update({'res_magnet': item.get('hy_magnet')})
        res_data.update({'res_contexts': item.get('hy_contexts')})
        res_data.update({'res_send_time': item.get('hy_send_time')})
        res_data.update({'res_author': item.get('hy_author')})
        res_data.update({'res_author_url': item.get('hy_author_url')})
        res_data.update({'res_publisher': item.get('hy_publisher')})
        res_data.update({'res_publisher_url': item.get('hy_publisher_url')})
        res_data.update({'res_type': item.get('hy_type')})
        res_data.update({'res_type_url': item.get('hy_type_url')})
        res_data.update({'res_size': item.get('hy_size')})
        self.write_xml_res(res_data=res_data)

    def write_xml_res(self, res_data):
        resource_node = self.xml_root.appendChild(self.xml_doc.createElement('resource'))
        for i in res_data.items():
            res_node = resource_node.appendChild(self.xml_doc.createElement(i[0]))
            print(i)
            res_node.appendChild(self.xml_doc.createTextNode(i[1]))
