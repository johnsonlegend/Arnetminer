# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArnetminerItem(scrapy.Item):
    name = scrapy.Field();
    agg_cita = scrapy.Field();
    h_index = scrapy.Field();
    G_index = scrapy.Field();
    pub_overyear = scrapy.Field();
    pass
