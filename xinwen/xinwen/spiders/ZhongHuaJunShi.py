# -*- coding: utf-8 -*-
import re

import scrapy
from scrapy import Selector, Request

from xinwen.items import XinwenItem


class ZhonghuajunshiSpider(scrapy.Spider):
    name = 'ZhongHuaJunShi'
    allowed_domains = ['military.china.com']
    start_urls = ['https://military.china.com/',
                  "https://military.china.com/news/",
                  "https://military.china.com/news2/",
                  # "https://military.china.com/kangzhan70/zhjw/",
                  # "https://military.china.com/historypic/",
                  # "https://military.china.com/jxkt/",
                  "https://military.china.com/aerospace/special/"
                  ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url,callback=self.parse_url,dont_filter=False)

    # // a // b / @ abc
    # 指的是文档中所有a元素的属性为abc的后代b元素（包括子代元素）（多级）；
    # // a / b / @ abc
    # 指的是文档中所有a元素的属性为abc的子代b元素（一级）；
    # / a / b / @ abc
    # 指的是根节点b元素的属性为abc的子代b元素（一级）；

    def parse_url(self, response):
        body = response.body.decode("utf-8")
        patter = re.compile('<a href="https://military.china.com/(.*?)" target="_blank"')
        urls = set(patter.findall(body))

        for url in urls:
            if url.endswith(".html"):
                url = url.replace(".html","_all.html")
                url = "https://military.china.com/" + url
                yield Request(url, callback=self.parse_content, dont_filter=False)
            else:
                url = "https://military.china.com/" + url
                # print(url + "\n")
                yield Request(url, callback=self.parse_url, dont_filter=False)


    def parse_content(self, response):
        selector = Selector(response)
        item = XinwenItem()
        item['title'] = selector.xpath('//h1[@class="article-main-title"]/text()').extract_first()
        item['time'] = selector.xpath(
            '//*[@id="js-article-title"]/*/div[@class="time-source"]/span[@class="time"]/text()').extract_first()
        item['source'] = selector.xpath('//*[@class="source"]/a/text()|//*[@class="source"]/text()').extract_first()
        item['content'] = selector.xpath('//*[@id="chan_newsDetail"]').xpath('string(.)').extract()[0].strip()
        print(item)
        yield item
        result = selector.xpath('//*[@id="js-column-list"]').extract()
        if result:
            pattern = re.compile('<a href="(.*?)" target="_blank">')
            urls = set(pattern.findall(result[0]))
            for url in urls:
                url = url.replace(".html", "_all.html")
                yield Request(url, callback=self.parse_content,dont_filter=False)


