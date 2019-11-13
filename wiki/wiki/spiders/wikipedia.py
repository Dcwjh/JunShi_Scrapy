# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

import re

from wiki.items import EntityItem
from wiki.items import RelationItem


class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['wikipedia.hk.wjbk.site']
    start_urls = ['https://wikipedia.hk.wjbk.site/baike-Portal:军事']
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }
    i = 0

    # 开始链接爬虫
    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_first,headers=self.headers)


    # 分类：标签实体 手动分类
    def parse_first(self, response):
        item_entity = EntityItem()

        list1 = response.xpath('//*[@id="mw-content-text"]/').extract_first()
        list2 = response.xpath('//*[@id="mw-content-text"]//').extract_first()


