# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class FileItem(scrapy.item.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    file_urls = scrapy.item.Field()
    files = scrapy.item.Field()

