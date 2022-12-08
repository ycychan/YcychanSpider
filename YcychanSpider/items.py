# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YcychanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class LzacgItem(scrapy.Item):
    lz_title = scrapy.Field()
    lz_url = scrapy.Field()
    lz_author = scrapy.Field()
    lz_type = scrapy.Field()
    lz_images_urls = scrapy.Field()
    lz_downlinks = scrapy.Field()
    lz_contexts = scrapy.Field()
    lz_send_time = scrapy.Field()
    lz_other = scrapy.Field()
    files = scrapy.Field()


class DmhyItem(scrapy.Item):
    hy_title = scrapy.Field()
    hy_url = scrapy.Field()
    hy_pikpak = scrapy.Field()
    hy_magnet = scrapy.Field()
    hy_contexts = scrapy.Field()
    hy_send_time = scrapy.Field()
    hy_author = scrapy.Field()
    hy_author_url = scrapy.Field()
    hy_publisher = scrapy.Field()
    hy_publisher_url = scrapy.Field()
    hy_type = scrapy.Field()
    hy_type_url = scrapy.Field()
    hy_size = scrapy.Field()
