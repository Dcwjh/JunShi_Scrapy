# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request

import re

from wiki.items import EntityItem
from wiki.items import RelationItem


class WikipediaSpider(scrapy.Spider):
    name = 'wikipedia'
    allowed_domains = ['wikipedia.hk.wjbk.site']
    start_urls = ['https://wikipedia.hk.wjbk.site/baike-Portal:%E8%BB%8D%E4%BA%8B']
    headers = {
        "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36"
    }

    # 开始链接爬虫
    def start_requests(self):
        yield Request(url=self.start_urls[0], callback=self.parse_first,headers=self.headers)


    # 分类：标签实体 手动分类
    def parse_first(self, response):
        list1 = response.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr/td/div[5]/div[4]/div[1]/table/tbody/tr/td[1]/div').extract_first()
        list2 = response.xpath('//*[@id="mw-content-text"]/div/table/tbody/tr/td/div[5]/div[4]/div[1]/table/tbody/tr/td[2]/div').extract_first()

        pattern = re.compile('<a href="(.*?)" .*?">(.*?)</a>')
        result1 = pattern.findall(list1)

        # 首页列表
        items1 = EntityItem()
        for index in range(1,len(result1)):
            items1["entity1"] = result1[index][1]
            items1["label"] = "label"
            items1["entity2"] = "战争"
            yield items1
            yield Request(url=result1[index][0], callback=self.parse_second, headers=self.headers)
            # with open('entity.csv','a',encoding="utf-8") as file:
            #     file.writelines(result1[index][1] + ",label,战争\n")


        # 军事列表
        items2 = EntityItem()
        result2 = pattern.findall(list2)
        for index in range(1, len(result2)):
            items2["entity1"] = result2[index][1]
            items2["label"] = "label"
            items2["entity2"] = "军事"
            yield items2
            yield Request(url=result2[index][0], callback=self.parse_second, headers=self.headers)

        result2 = pattern.findall(list2)
        # print(result2[29])
        # yield Request(url=result2[29][0],callback=self.parse_second,headers=self.headers)

    # 分类：自动分类
    def parse_second(self,response):
        label = response.xpath('//*[@id="firstHeading"]/text()').extract_first()[3:]
        items = response.xpath('//*[@id="mw-subcategories"]').extract()
        print(len(items))
        for item in items:
            pattern = re.compile('<a href="(.*?)" .*?>(.*?)</a>‎')
            results = pattern.findall(item)
            url = results[0][0]
            # for result in results:
            #     with open("测试.csv", "a", encoding="utf-8") as file:
            #         file.write(result[1] + ",label," + label + "\n")
            #         yield Request(url=result[0], callback=self.parse_relation, headers=self.headers)
        # print(url)
        # yield Request(url=url, callback=self.parse_relation, headers=self.headers)
        # if "baike-Category" in url:
        #     yield Request(url=url, callback=self.parse_relation, headers=self.headers)

    def parse_relation(self, response):
        pass



        # print(response.body.decode("utf-8"))
        # print(response.body.decode("utf-8"))

#