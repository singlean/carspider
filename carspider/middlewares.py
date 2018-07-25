# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

from carspider.settings import USER_AGENT_LIST
import random

class RandomUserAgent(object):

    def process_request(self, request, spider):

        UA = random.choice(USER_AGENT_LIST)
        request.headers["User-Agent"] = UA

