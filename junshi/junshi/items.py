# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JunshiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # _id = scrapy.Field()
    # abstracts = scrapy.Field()
    country = scrapy.Field()
    # country_image_url = scrapy.Field()
    entity = scrapy.Field()
    feature = scrapy.Field()
    # id = scrapy.Field()
    # info_image_url = scrapy.Field()
    redirect_url = scrapy.Field()
    description = scrapy.Field()
    properties = scrapy.Field()
