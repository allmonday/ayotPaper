#coding: utf-8
import re
import scrapy
from kimiaj.items import PacificItem 

class PacificSpider(scrapy.Spider):

    name = 'pacific'
    start_urls = ['https://bbs.pcbaby.com.cn/forum-1914.html']

    def parse(self, response):

        date_re = re.compile(r'\[*.?\]')
        articles = response.css('.resultArea>.singleResult')
        next_page = str(int(response.css('.pageNum .active ::text').extract_first()) + 1)

        for article in articles:
            try:
                item = PacificItem()
                item['title'] = ''.join(article.css('h3>a ::text').extract())
                item['link'] = article.css('h3>a ::attr(href)').extract_first()
                item['desc'] = ''.join(article.css('.textA::text').extract()).strip()
                item['author'] = article.css('.relate a::text').extract()[0]
                item['date'] = (article.css('h3 .date::text').extract_first()).split('[')[-1][:-1]
                yield item
            except Exception as e:
                print e
                print next_page
                continue

        if next_page:
            yield scrapy.Request('https://bbs.pcbaby.com.cn/forum-{}.html'.format(next_page), callback=self.parse)
