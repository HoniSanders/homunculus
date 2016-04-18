# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class InjuryItem(scrapy.Item):
    name = scrapy.Field()
    team = scrapy.Field()
    position = scrapy.Field()

    # 15 day, 10 day etc
    dl_type = scrapy.Field()

    injury_type = scrapy.Field()