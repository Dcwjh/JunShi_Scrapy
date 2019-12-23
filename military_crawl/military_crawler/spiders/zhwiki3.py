import scrapy
import re
from military_crawler.items import ZhWikiKeyword
from military_crawler.items import NewTriple

# 中和了维基百科和互动百科


# 基于中文维基的军事分类,爬取与军事相关的关键词,再利用互动百科和wikidata进行属性扩展


class zhwiki(scrapy.Spider):
    name = 'zhwiki3'
    limit_depth = 15  # 爬取的最大深度
    # ['军事战争','军事人物','军事文化','军事经济学','军事史']
    category_names = ["军事之最","军事航空","军事书籍","军事外交","战争史"]

    def start_requests(self):
        for category_name in self.category_names:
            start_urls = 'https://wikipedia.hk.wjbk.site/baike-Category:%s' % category_name
            yield scrapy.Request(url=start_urls, callback=self.parse, meta={"label": category_name})

    def parse(self, response):
        label = ""
        if 'depth' in response.meta:
            depth = response.meta['depth']
            label = response.meta["label"]
        else:
            depth = 0
        depth += 1
        if depth <= self.limit_depth:
            # 爬取子分类类
            sub_category_list = response.xpath(
                '//*[@id="mw-subcategories"]//div[@class="CategoryTreeItem"]//a')
            for index in range(len(sub_category_list)):
                sub_category_url = sub_category_list[index].xpath('./@href').extract_first()  # 子类链接
                print(sub_category_url)
                yield scrapy.Request(sub_category_url, callback=self.parse,
                                     meta={'depth': depth, "label": label})
            #  叶子节点，最终实体， 就是子分类下面的属性
            entity_list = response.xpath('//*[@id="mw-pages"]//li/a')
            for index in range(len(entity_list)):
                entity_name = entity_list[index].xpath('./@title').extract_first()
                entity_url = entity_list[index].xpath('./@href').extract_first()
                keyword = ZhWikiKeyword()
                entity_name = re.sub('\\(.*\\)', '', entity_name).strip()  # 去掉entity_name去掉（）后面的内容
                if 'Template' in entity_url or 'Portal' in entity_url:
                    pass
                else:
                    if "列表" in entity_name:
                        keyword['title'] = entity_name
                        keyword['url'] = entity_url
                        print(keyword)
                        yield keyword
                    # print(type(entity_name))
                    yield scrapy.Request(
                        url='http://www.baike.com/wiki/%s' % entity_name, callback=self.parse_baike,
                                       meta={'title': entity_name, 'label': label})

    def parse_baike(self, response):
        title = response.meta['title']
        label = response.meta['label']
        name = response.xpath('//*[@class="content-h1"]/h1/text()').extract_first()  # 提取名称
        if name:
            label_list = response.xpath('//*[@id="openCatp"]/a/@title').extract()  # 提取互动百科所分配的类别
            for entity in label_list:
                newtriple = NewTriple()
                newtriple['e1'] = title
                newtriple['r'] = '属于'
                newtriple['e2'] = entity
                newtriple['label'] = label
                print(newtriple)
                yield newtriple

            td_list = response.xpath('//*[@id="datamodule"]//td')
            for td in td_list:
                if td.xpath('./strong') and td.xpath('./span'):
                    key = td.xpath('./strong').xpath('string(.)').extract_first()[0:-1].strip().replace(' ', '')
                    value = ''
                    for span in td.xpath('./span'):
                        value += span.xpath('string(.)').extract_first().strip().replace(' ', '')
                    newtriple = NewTriple()
                    newtriple['e1'] = title
                    newtriple['r'] = key
                    newtriple['e2'] = value
                    newtriple["label"] = label

                    print(newtriple)
                    yield newtriple
