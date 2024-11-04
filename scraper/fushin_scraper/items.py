# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Post(scrapy.Item):
    article_date = scrapy.Field()
    short_title = scrapy.Field()
    long_title = scrapy.Field()
    url = scrapy.Field()