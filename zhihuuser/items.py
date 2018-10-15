# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UserItem(scrapy.Item):
    # define the fields for your item here like:
    id = scrapy.Field()
    name = scrapy.Field()
    avatar_url = scrapy.Field()
    headline = scrapy.Field()
    url_token = scrapy.Field()
    url = scrapy.Field()
    gender = scrapy.Field()
    type = scrapy.Field()
    
    description = scrapy.Field()
    locations = scrapy.Field()
    following_question_count = scrapy.Field()
    thanked_count = scrapy.Field()
    badge = scrapy.Field()
    business = scrapy.Field()
    employments = scrapy.Field()
    educations = scrapy.Field()
