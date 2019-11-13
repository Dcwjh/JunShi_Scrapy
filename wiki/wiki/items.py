# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class EntityItem(scrapy.Item):
    ID = scrapy.Field()
    name = scrapy.Field()
    label = scrapy.Field()

class RelationItem(scrapy.Item):
    ID1 = scrapy.Field()
    ID2 = scrapy.Field()
    relation = scrapy.Field()

