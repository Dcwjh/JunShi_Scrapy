from wiki.items import EntityItem,RelationItem


class EntityPipeline(object):
    def open_spider(self, spider):
        self.file_entity = open("nodes.csv",'a+', encoding="utf-8")
        self.file_relation = open("edges.csv", 'a+', encoding="utf-8")
        self.file_keyword = open("Keyword.txt",'a+', encoding="utf-8")

    def process_item(self, item, spider):
        if isinstance(item,EntityItem):
            if item["ID"] and item["name"]:
                self.file_entity.write(item["ID"] + "," + item["name"]+ "," + item["label"] + "\n")
        if isinstance(item, RelationItem):
            if item["ID1"] and item["ID2"]:
                self.file_relation.write(item["ID1"] + "," + item["ID2"] + "," + item["relation"] + "\n")
        return item

        # 在爬虫停止的时候清理一些事情

    def close_spider(self, spider):
        self.file_relation.close()
        self.file_entity.close()

# class RelationPipeline(object):
#     pass
#     def open_spider(self, spider):
#         self.file = open("relation.csv",'a+', encoding="utf-8")
#
#     def process_item(self, item, spider):
#         if item["entity1"] and item["entity2"]:
#             self.file.write(item["entity1"] + "," + item["relation"] + "," + item["entity2"] + "\n")
#         return item
#
#         # 在爬虫停止的时候清理一些事情
#
#     def close_spider(self, spider):
#         self.file.close()

