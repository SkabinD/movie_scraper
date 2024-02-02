# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class MovieItem(scrapy.Item):
    name = scrapy.Field()
    genre = scrapy.Field()
    country = scrapy.Field()
    director = scrapy.Field()
    year = scrapy.Field()

class MovieItemExtended(MovieItem):
    name = scrapy.Field()
    genre = scrapy.Field()
    country = scrapy.Field()
    director = scrapy.Field()
    year = scrapy.Field()
    imdb_score = scrapy.Field()