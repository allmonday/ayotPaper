#coding: utf-8
import re
import scrapy
from kimiaj.items import KimiajItem

class TianyaSpider(scrapy.Spider):

    name = 'tianya'
    start_urls = ['http://search.tianya.cn/bbs?q=%E4%BA%8C%E5%AD%A9&pid=']

    def parse(self, response):

        articles = response.css('.searchListOne>ul>li:not(#search_msg)')
        tag = re.compile(r'<.*?>')
        next_page = response.css('.long-pages>strong+a ::text').extract_first()

        for article in articles:
            try:
                item = {}
                item['title'] = ''.join(article.css('div>h3>a ::text').extract())
                item['link'] = article.css('div>h3>a ::attr(href)').extract_first()
                item['author'] = article.css('.source a::text').extract()[1]
                item['date'] = article.css('.source span::text').extract()[0]
                item['reply'] = article.css('.source span::text').extract()[1]
                link = article.css('div>h3>a ::attr(href)').extract_first()
                yield scrapy.Request(link, callback=self.parse_main_content, meta=item)

            except Exception as e:
                print e
                print next_page
                continue

        if next_page:
            yield scrapy.Request('http://search.tianya.cn/bbs?q=%E4%BA%8C%E5%AD%A9&pn={}'.format(next_page), callback=self.parse)

    def parse_main_content(self, response):

        main_line = response.css(".atl-con-bd")[0]
        item = KimiajItem()
        elder_info = response.meta
        item['title'] = elder_info['title']
        item['link'] = elder_info['link']
        item['author'] = elder_info['author']
        item['date'] = elder_info['date']
        item['reply'] = elder_info['reply']
        item['content'] = main_line.css(".bbs-content::text").extract_first().replace("<br>", "").strip()

        yield item
