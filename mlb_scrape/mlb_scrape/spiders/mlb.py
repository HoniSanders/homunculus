# -*- coding: utf-8 -*-
import scrapy
import os
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor

import json

from datetime import datetime
from datetime import date, timedelta

now_time = datetime.now() - timedelta(days=1)
year = str(now_time.year)
month = str(now_time.month).zfill(2)
day = str(now_time.day).zfill(2)

import ingest

class MlbSpider(CrawlSpider):
    name = "mlb"

    allowed_domains = ["mlb.com"]
    start_urls = (
        'http://gd2.mlb.com/components/game/mlb/year_{}/month_{}/day_{}'.format(year, month, day),
    )
    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('game_events.json', )), callback='parse_item'),
        # and follow links from them (since no callback means follow=True by default)

        Rule(LinkExtractor(deny_extensions=('plist', 'xml'), allow=('month_{}/?$'.format(month), 'day_{}/?$'.format(day), '/gid_{}_{}_{}_.+'.format(year,month,day) ), deny=('notifications','linescore', 'pitchers', 'media', 'inning' 'premium', 'batters',))),
    )

    def parse_item(self, response):
        url = response.url
        name = url.rsplit("/")[-2]
        print "my name=", name
        jobj = json.loads( response.body_as_unicode() )
        basedir = os.path.dirname(os.path.realpath(__file__))
        output_dir = os.path.join(basedir, "../..", "output", year)
        # output_dir = "/tmp/mlb_output/{}".
        # print output_dir
        # import sys; sys.exit()
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)
        target_path = os.path.join(output_dir, '{}.json'.format(name))
        with open(target_path, 'w') as outfile:
        #   json.dump(jobj, outfile)
            ingest.process(jobj, name)
