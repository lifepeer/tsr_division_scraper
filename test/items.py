# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class Poll(Item):
    name = Field()
    code = Field()
    totals = Field()
    aye = Field()
    no = Field()
    abstain = Field()
    end = Field()
    anomaly = Field()
    location = Field()
