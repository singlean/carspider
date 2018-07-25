# -*- coding: utf-8 -*-
import scrapy,re
from urllib.parse import urljoin
from copy import deepcopy
from scrapy_redis.spiders import RedisSpider
import pprint

class AkcarSpider(RedisSpider):
    name = 'akcar'
    allowed_domains = ['com.cn']
    # start_urls = ['http://newcar.xcar.com.cn/car/']
    redis_key = "akcar"

    def parse(self, response):

        # 正则匹配url地址
        regex = r"</span>(.*?)</a></li><li><a href=\"(http://newcar\.xcar\.com\.cn/car/0-0-0-0-\d+?-0-0-0-0-0-0-0/)\""
        sub1 = r"</a></li><li class=\"name\">.{1}</li><li><a href=\""
        sub2 = r"\" data-id.*</span>"
        brand_list = re.findall(regex, response.body.decode("gbk"))

        for i in brand_list:
            item = {}
            items = {}
            if "class=\"name\">" in i[0]:
                i_list = []
                # 去除无用信息
                i0 = re.sub(sub1,"++",i[0])
                i0 = re.sub(sub2,"++",i0)
                i0 = i0.split("++")
                i_list.extend(i0)
                i_list.append(i[1])
                # 两个url地址分开请求
                item["brand_name"] = i_list[0]
                item["brand_href"] = i_list[1]

                items["brand_name"] = i_list[2]
                items["brand_href"] = i_list[3]

                # 请求items的数据
                yield scrapy.Request(
                    url=items["brand_href"],
                    callback=self.parse_brand_list,
                    meta={"item":items}
                )
            else:
                item["brand_name"] = i[0]
                item["brand_href"] = i[1]

            # 请求item的数据
            yield scrapy.Request(
                url=item["brand_href"],
                callback=self.parse_brand_list,
                meta={"item": item}
            )

    def parse_brand_list(self,response):
        item = response.meta["item"]
        # 汽车信息列表
        div_list = response.xpath("//div[@class='car_list']/div")
        for div in div_list:
            item["car_url"] = div.xpath("./a/@href").extract_first()
            item["car_name"] = div.xpath("./a/img/@title").extract_first()
            item["car_img"] = div.xpath("./a/img/@src").extract_first()

            if item["car_url"]:
                item["car_url"] = urljoin(response.url,item["car_url"])
                yield scrapy.Request(
                    url=item["car_url"],
                    callback=self.parse_car_detail,
                    meta={"item":deepcopy(item)}
                )

    def parse_car_detail(self,response):
        item = response.meta["item"]
        # 参考价格
        item["car_reference_price"] = response.xpath("//div[@class='data_zd price_menu_box']/span/text()").extract_first()
        # 汽车级别 双重列表生产式去除空白字符
        item["car_level"] = response.xpath("//div[@class='data_list']/ul/li[1]/text()").extract()
        item["car_level"] = [x for x in [i.strip() for i in item["car_level"] if i] if x]
        # 结构　双重列表生产式去除空白字符
        item["car_structure"] = response.xpath("//div[@class='data_list']/ul/li[2]/text()").extract()
        item["car_structure"] = [x for x in [i.strip() for i in item["car_structure"] if i ] if x]
        # 油耗　双重列表生产式去除空白字符
        item["car_consume"] = response.xpath("//div[@class='data_list']/ul/li[3]/text()").extract()
        item["car_consume"] = [x for x in [i.strip() for i in item["car_consume"] if i ] if x]
        # 排放
        item["car_discharge"] = response.xpath("//div[@class='data_list']/ul/li[4]/a/text()").extract()
        # 保修　双重列表生产式去除空白字符
        item["car_warranty"] = response.xpath("//div[@class='data_list']/ul/li[5]/text()").extract()
        item["car_warranty"] = [x for x in [i.strip() for i in item["car_warranty"] if i] if x]
        # 变速箱
        item["car_var"] = response.xpath("//div[@class='data_list']/ul/li[6]/a/text()").extract_first()

        yield item





































