# -*- coding: utf-8 -*-

# see: http://doc.scrapy.org/en/latest/topics/items.html

import re
from scrapy import Item, Field

last_date = ''
this_year = ''

class IgokisenNewsItem(Item):
    date   = Field()
    nation = Field()
    game   = Field()
    link   = Field()

    def __init__(self, year):
        global this_year
        this_year = year
        Item.__init__(self)

    def parse(self, row):
        global last_date
        self['date']   = last_date = self.rowDate(row)
        self['nation'] = self.rowNation(row)
        self['game']   = self.rowGame(row)
        self['link']   = self.rowLink(row)
        return self

    def rowDate(self, row):
        global this_year
        str = self.pluck(row, 'td/text()')
        if re.match('\d\d-\d\d', str):
            return '%s-%s' % (this_year, str)
        else:
            return last_date

    def rowNation(self, row):
        return self.pluck(row, 'td/span/text()')

    def rowLink(self, row):
        return self.pluck(row, 'td/a/@href')

    def rowGame(self, row):
        return self.pluck(row, 'td/a/text()')

    def pluck(self, row, selector):
        text = row.xpath(selector).extract()
        return text[0] if len(text) else ''
