# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TorrentObject(scrapy.Item):
    name = scrapy.Field()
    size = scrapy.Field()
    reg = scrapy.Field()
    hash = scrapy.Field()
    seeders = scrapy.Field()
    leeches = scrapy.Field()
    url = scrapy.Field()
