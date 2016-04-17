# -*- coding: utf-8 -*-

# Scrapy settings for mlb_scrape project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'mlb_scrape'

SPIDER_MODULES = ['mlb_scrape.spiders']
NEWSPIDER_MODULE = 'mlb_scrape.spiders'

ITEM_PIPELINES = {
    'mlb_scrape.pipelines.MlbScrapePipeline': 300,
}

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'mlb_scrape (+http://www.yourdomain.com)'
