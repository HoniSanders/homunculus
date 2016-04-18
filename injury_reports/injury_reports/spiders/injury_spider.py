import scrapy
from injury_reports.items import InjuryItem

class InjurySpider(scrapy.Spider):
    name = "injuries"
    allowed_domains = ["yahoo.com"]
    start_urls = [
        "https://baseball.fantasysports.yahoo.com/b1/injuries"
    ]

    def parse(self, response):
        for injury_row in response.xpath('//tr[@class="Alt"]'):
            item = InjuryItem()
            item['name'] = injury_row.xpath('.//a[contains(@class, "name F-link")]/text()').extract()[0]

            team_position = injury_row.xpath('.//span[@class="Fz-xxs"]/text()').extract()[0]
            team_position_components = team_position.split('-')
            item['team'] = team_position_components[0].strip()
            item['position'] = team_position_components[1].strip()

            item['dl_type'] = injury_row.xpath('.//span[contains(@class, "ysf-player-status")]/text()').extract()[0]

            item['injury_type'] = injury_row.xpath('.//td[@class="Last Ta-start"]/div/text()').extract()[0]
            print item

        