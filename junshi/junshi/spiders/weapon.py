# -*- coding: utf-8 -*-
import scrapy
import re
import json
from junshi.items import JunshiItem
from scrapy import Request
from scrapy import Selector


class WeaponSpider(scrapy.Spider):
    name = 'weapon'
    allowed_domains = ['weapon-p.china.com', 'military.china.com']
    list_weapon = ["飞行器", "舰船舰艇", "枪械与单兵", "坦克装甲车辆", "火炮", "导弹武器", "太空装备", "爆炸物"]
    start_urls = 'https://weapon-p.china.com/?&weapon_type={type}&page=1'

    def start_requests(self):
        for index in range(len(self.list_weapon)):
            yield Request(self.start_urls.format(type=self.list_weapon[index]), callback=self.parse_weapon)

    def parse_weapon(self, response):
        res = response.text
        pattern = re.compile("{.*}")
        txt = pattern.search(res).group()
        result = json.loads(txt)
        item = JunshiItem()
        resultList = result['rows']
        for it in iter(resultList):
            for field in item.fields:
                if it.get(field):
                    item[field] = it.get(field)
                    if field == "redirect_url":
                        detail = it.get(field)
                        yield Request(url=detail, callback=self.parse_weapon_detail, meta=item)
        for index in range(2, result['totalPage']):
            pattern = re.compile("http.*page=")
            txt = pattern.search(response.url).group()
            next_url = txt + str(index)
            yield scrapy.Request(url=next_url, callback=self.parse_weapon)

    def parse_weapon_detail(self, response):

        item = JunshiItem()
        for field in item.fields:
            if response.meta.get(field):
                item[field] = response.meta[field]
        item['description'] = response.xpath('//*[@id="info-flow"]/div[1]/div[3]/p/text()').extract_first()
        properties = []
        tds = response.xpath('//*[@id="info-flow"]/div[1]/table//*/td').extract()
        for td in tds:
            pattern = re.compile("<td><em>(.*?)</em><p>(.*?)</p><")
            name = pattern.search(td).group(1)
            value = pattern.search(td).group(2)
            dic = {name:value}
            properties.append(dic)
        item['properties'] = properties

        yield item

        # yield item
        # tds = response.xpath('//*[@id="info-flow"]/div[1]/table//td').extract()
        # for td in tds:
        #     name = Selector(text=td).xpath('//em/text()').extract_first()
        #     value = Selector(text=td).xpath('//p/text()').extract_first()

