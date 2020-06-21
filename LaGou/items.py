# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class LagouItem(scrapy.Item):
    # define the fields for your item here like:
    job_url = scrapy.Field()
    job_name = scrapy.Field()
    salary = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    labels = scrapy.Field()
    publish_date = scrapy.Field()
    company = scrapy.Field()
    company_feature = scrapy.Field()
    company_public = scrapy.Field()
    company_size= scrapy.Field()
