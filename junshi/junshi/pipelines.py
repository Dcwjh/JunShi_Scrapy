# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json


class JunshiPipeline(object):
    def open_spider(self, spider):
        self.file = open("junshi.json",'w+')

    def process_item(self, item, spider):
        dict_data = dict(item)
        # 将字典转换成json字符串
        str_data = json.dumps(dict_data, ensure_ascii=False) + '\n'
        # 写入文件
        self.file.write(str_data)

        return item

        # 在爬虫停止的时候清理一些事情

    def close_spider(self, spider):
        self.file.close()

