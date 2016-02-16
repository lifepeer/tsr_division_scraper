# -*- coding: utf-8 -*-

# Scrapy settings for test project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'test'

SPIDER_MODULES = ['test.spiders']
NEWSPIDER_MODULE = 'test.spiders'

ITEM_PIPELINES = ['test.pipelines.MongoDBPipeline', ]

MONGODB_SERVER = 'ds031893.mongolab.com'
# MONGODB_PORT = 27017
# MONGODB_DB = 'test'
MONGODB_PORT = 31893
MONGODB_URI = 'mongodb://lifepeer:KGCu&4Yz@ds031893.mongolab.com:31893/mhoctest'
MONGODB_DB = 'mhoctest'
MONGODB_COLLECTION = 'votes'

#DOWNLOAD_DELAY = 1

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'test (+http://www.yourdomain.com)'
