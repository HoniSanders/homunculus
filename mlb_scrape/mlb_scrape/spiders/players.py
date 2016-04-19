# -*- coding: utf-8 -*-
import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


import json

import json

from pymongo import MongoClient

uri = "mongodb://mlb:hellodata@18.42.2.112/?authMechanism=SCRAM-SHA-1"
client = MongoClient(uri).baseball
year = "2016"
class PlayerSpider(CrawlSpider):
    name = "players"

    allowed_domains = ["mlb.com"]
    start_urls = (
        'http://gd2.mlb.com/components/game/mlb/year_{}/'.format(year),
    )
    rules = (
        # Extract links matching 'item.php' and parse them with the spider's method parse_item
        Rule(LinkExtractor(allow=('players.xml', )), callback='parse_item'),
        # and follow links from them (since no callback means follow=True by default)

        # and follow links from them (since no callback means follow=True by default)

        Rule(LinkExtractor(deny_extensions=('plist', 'json'), allow=('month_0[4-9]/?$', 'day_\d{2}/?$', '/gid_'+year+'_\d{2}_\d{2}_.*' ), deny=('atv_preview.xml', 'notifications','linescore', 'pitchers', 'media', 'inning' 'premium', 'batters' ))),

    )

    def parse_item(self, response):
        soup = BeautifulSoup(response.body)
        players = soup.find_all("player")
        for p in players:
            try:
                pid = p.get("id")
                name = p.get("first") + " " + p.get("last")
                pdict  = {"name": name,
                          "_id" : "{}_{}".format(year, pid),
                          "year": int(year),
                          "player_id" : pid,
                          "team_abbrev": p.get("team_abbrev"),
                          "position": p.get("position")}
                client.players.insert(pdict)
            except Exception, e:
                print "err", e
        print "end players"
