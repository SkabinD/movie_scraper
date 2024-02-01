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
    # imdb = scrapy.Field()
    url = scrapy.Field() # For debug purposes
