# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class Post(scrapy.Item):
    date = scrapy.Field()
    title = scrapy.Field()
    title_detail = scrapy.Field()
    url = scrapy.Field()