# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

import json

class MlbScrapeItem(scrapy.Item):
    # define the fields for your item here like:
    #name = scrapy.Field()

    def __init__(self, raw):
        jobj = json.loads(raw)
        for key in jobj:
            setattr(self, key, jobj[key])
    
