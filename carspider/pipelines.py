# -*- coding: utf-8 -*-

from pymongo import MongoClient


class CarPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["car"]

    def process_item(self, item, spider):
        if spider.name == "car":
            self.collection.insert(item)
            print("保存成功")

        return item


class AkCarPipeline(object):

    def open_spider(self, spider):
        # 创建一个mongo客户端对象
        client = MongoClient()
        # 创建一个集合保存数据
        self.collection = client["spider"]["akcar"]

    def process_item(self, item, spider):
        if spider.name == "akcar":
            self.collection.insert(item)
            print("保存成功")

        return item