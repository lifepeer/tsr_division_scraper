# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector

from scrapy.contrib.linkextractors import LinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule

from pymongo import MongoClient

import dateutil.parser as dparser
from datetime import datetime, timedelta

from test.items import Poll

class SpiderMan(CrawlSpider):
    name = "peter"
    allowed_domains = ["thestudentroom.co.uk"]
    start_urls = [
    "http://www.thestudentroom.co.uk/forumdisplay.php?f=145&page=1",
    ]

    rules = (
    Rule(LinkExtractor(allow=r'showthread.php\?t=[0-9]+', deny=r'showthread.php\?t=[0-9]+&page=[0-9]+', restrict_xpaths='//table[@id="threadlist"]//td[@class="title"]')),
    # Rule(LinkExtractor(allow=r'showthread.php\?t=3488069', deny=r'showthread.php\?t=[0-9]+&page=[0-9]+', restrict_xpaths='//table[@id="threadlist"]//td[@class="title"]')),
    Rule(LinkExtractor(allow=r'poll.php\?pollid=[0-9]+&do=showresults'), callback='parse_item'),
    )

    def parse_item(self, response):
        polls = Selector(response).xpath('//li[@class="poll-container"]')
        # client = MongoClient('localhost', 3001)
        client = MongoClient('mongodb://lifepeer:KGCu&4Yz@ds031893.mongolab.com:31893/mhoctest')

        for poll in polls:
            item = Poll()
            fullName = ''.join(response.selector.xpath('//div[@id="breadcrumb"]/span[last()]/a/text()').extract()).split()
            item['code'] = fullName[0]

            date = ''.join(poll.xpath('//div[@class="poll-close-date"]/text()').extract()).replace('\n', '')
            date = dparser.parse(date, fuzzy=True, dayfirst=True)

            # If the vote is still open, remove the document and add its new version
            if date > datetime.now() - timedelta(days=1):
                # client.meteor.votes.remove({'code': item['code']})
                client.mhoctest.votes.remove({'code': item['code']})

            # If the document already exists and the vote has ended, continue
            # if client.meteor.votes.find({'code': item['code']}).count() is not 0:
            if client.mhoctest.votes.find({'code': item['code']}).count() is not 0:
                continue

            item['end'] = str(date)
            item['name'] = ' '.join(fullName[2:])
            item['totals'] = map(int, poll.xpath('//div[@class="poll_results_votes"]//text()').extract())
            item['totals'].append(sum(item['totals']))
            item['aye'] = {'users': poll.xpath('//div[@class="poll-result-option"][1]//a[@class="username"]//text()').extract(),
            'num': item['totals'][0]}
            item['no'] = {'users': poll.xpath('//div[@class="poll-result-option"][2]//a[@class="username"]//text()').extract(),
            'num': item['totals'][1]}
            item['abstain'] = {'users': poll.xpath('//div[@class="poll-result-option"][3]//a[@class="username"]//text()').extract(),
            'num': item['totals'][2]}
            if item['totals'][0] == len(item['aye']['users']) \
                and item['totals'][1] == len(item['no']['users']) \
                and item['totals'][2] == len(item['abstain']['users']):
                item['anomaly'] = False
            else:
                item['anomaly'] = True
            item['location'] = ''.join(response.selector.xpath('//div[@id="breadcrumb"]/span[last()]/a/@href').extract())

            return item
