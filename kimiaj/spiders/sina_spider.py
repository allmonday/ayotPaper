#coding: utf-8
import re
import scrapy
from kimiaj.items import SinaItem

class TianyaSpider(scrapy.Spider):

    name = 'sina'
    start_urls = ['http://search.sina.com.cn/?q=%B6%FE%BA%A2&range=title&c=news&sort=time']

    def parse(self, response):

        articles = response.css('#result .box-result')
        next_page = str(int(response.css('.pagebox .pagebox_cur_page::text').extract_first()) + 1)
        print 'nextpage: {}'.format(next_page)

        for article in articles:
            try:
                item = SinaItem()
                temps = article.css('.r-info>h2>.fgray_time::text').extract_first().split(' ')
                source = temps[0]
                date = temps[1]
                item['title'] = ''.join(article.css('.r-info>h2>a::text').extract())
                item['link'] = article.css('.r-info>h2>a ::attr(href)').extract_first()
                item['desc'] = article.css('.r-info .content::text').extract_first()
                item['date'] = date
                item['source'] = source
                yield item
            except Exception as e:
                print e
                print next_page
                continue

        if next_page:
            yield scrapy.Request('http://search.sina.com.cn/?q=%B6%FE%BA%A2&range=title&c=news&sort=time&col=&source=&from=&country=&size=&time=&a=&page={}&pf=2131425462&ps=2134309112&dpc=1'.format(next_page), callback=self.parse)
