# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from aitaotuIMG.items import AitaotuimgItem


class AissspiderSpider(CrawlSpider):
    name = 'AissSpider'
    allowed_domains = ['www.aitaotu.com']
    #https://www.aitaotu.com/tag/aiss.html
    start_urls = ['https://www.aitaotu.com/tag/maomengbang.html']

    rules = (
        #下一页链接提取，可以修改allow maomengbang
        Rule(LinkExtractor(allow=('/tag/maomengbang/\d+')), follow=True),
        #图片翻页
        Rule(LinkExtractor(allow=('/guonei/\d+'), restrict_xpaths=('//div[@class="pages"]')), callback='parse_item',
             follow=True),
        #子页面链接
        Rule(LinkExtractor(allow = ('/guonei/\d+'),restrict_xpaths=('//li/a[@class="Pli-litpic"]')),callback='parse_item',follow=True),


    )

    def parse_item(self, response):

        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()

        link_list = response.xpath('/html/body/div[3]/div[2]/div[@class="big-pic"]/div[@id="big-pic"]/p/a')
        for each in link_list:
            item=AitaotuimgItem()
            item['title'] = response.xpath('/html/body/div[3]/div[2]/div[2]/h2/text()').extract()[0]
            item['img_url'] = each.xpath('./img/@src').extract()[0]
            item['name']= each.xpath('./img/@alt').extract()[0]

            yield item

