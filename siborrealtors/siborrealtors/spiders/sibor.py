# -*- coding: utf-8 -*-
import scrapy
import math
import csv
import win32api


class SiborSpider(scrapy.Spider):
    name = 'sibor'
    
    def start_requests(self):
        base_url = "https://www.siborrealtors.com/agent/search?page={}"

        for i in range(1, 118):
            page_url = base_url.format(i)

            yield scrapy.Request(url=base_url, callback=page_parse)

    def page_parse(self, response):
        



    
