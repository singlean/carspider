# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider
import datetime,random


class CarSpider(RedisSpider):
    name = 'car'
    allowed_domains = ['com.cn']
    # start_urls = ['https://www.autohome.com.cn/car/']
    redis_key = "car"

    def parse(self, response):

        # 分类列表
        dd_list = response.xpath("//dl[@class='caricon-list']/dd")[1:13]
        for dd in dd_list:
            item = {}
            item["cate_href"] = "https://www.autohome.com.cn" + dd.xpath("./a/@href").extract_first()
            item["cate_name"] = dd.xpath("./a/span/text()").extract_first()

            yield scrapy.Request(
                url=item["cate_href"],
                callback=self.parse_cate_list,
                meta={"item":item}
            )

    def parse_cate_list(self,response):
        item = response.meta["item"]

        div_list = response.xpath("//div[@class='tab-content-item']/div[@class='uibox']")
        for div in div_list:
            item["brand_name"] = div.xpath(".//div[@class='h3-tit']/a/text()").extract_first()
            item["brand_href"] = "https:" + div.xpath(".//div[@class='h3-tit']/a/@href").extract_first()

            yield scrapy.Request(
                url=item["brand_href"],
                callback=self.parse_car_list,
                meta={"item":item}
            )

    def parse_car_list(self,response):
        item = response.meta["item"]

        div_list = response.xpath("//div[@class='tab-content-item current']/div[@class='list-cont']")

        for div in div_list:
            item["car_img"] = "https:" + div.xpath(".//div[@class='list-cont-img']/a/img/@src").extract_first()
            item["car_level"] = div.xpath(".//div[@class='main-lever-left']/ul/li[1]/span/text()").extract_first()
            item["car_url"] = div.xpath(".//div[@class='main-lever-left']/ul/li[2]/a/@href").extract_first()
            if item["car_url"]:
                item["car_url"] = "https://car.autohome.com.cn" + item["car_url"]
            item["car_structure"] = div.xpath(".//div[@class='main-lever-left']/ul/li[2]/a/text()").extract_first()
            item["car_engine"] = div.xpath(".//div[@class='main-lever-left']/ul/li[3]/span/a/text()").extract_first()
            item["car_var"] = div.xpath(".//div[@class='main-lever-left']/ul/li[4]/a/text()").extract_first()
            item["car_reference_price"] = div.xpath(".//span[@class='lever-price red']/span/text()").extract_first()
            item["car_score"] = div.xpath(".//span[@class='score-number']/text()").extract_first() if len(div.xpath(".//span[@class='score-number']/text()")) else None
            item["_id"] = self.create_mongodb_id()

            yield item

    # 自定义_id字段
    def create_mongodb_id(self):

        low_list = ["q","w","e","r","t","y","u","i","o","p","a","s","d","f","g","h","j","k","l","z","x",
              "c","v","b","n","m"]
        upp_list = [i.upper() for i in low_list]
        int_list = [1,2,3,4,5,6,7,8,9,0]

        low = random.choice(low_list) + random.choice(low_list)
        upp = random.choice(upp_list) + random.choice(upp_list)
        num = str(random.choice(int_list)) + str(random.choice(int_list))

        _id = datetime.datetime.now().strftime('%Y%m%d%H%M%S') + low + upp + num

        return _id










