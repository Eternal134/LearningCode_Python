# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from lxml import etree


class JwcSpider(scrapy.Spider):
    name = 'jwc'
#   allowed_domains = ['http://jwc.ahu.cn']
    start_urls = ['http://jwc.ahu.cn/main/']

    def parse(self, response):
        print(response)
        news = response.xpath("//table[@cellspacing='0'and @cellpadding='1']/tbody/tr")
        for new in news:
            content_url = new.xpath("./td[@height='22']/a/@href").extract()[0]
            yield scrapy.Request("http://jwc.ahu.cn/main/" + content_url , callback = self.parse_content)
    
    def parse_content(self , response):
        item = NewsItem()
        item['title'] = response.xpath("//tbody/tr[2]//div/b/text()").extract()[0]
        item['datetime'] = response.xpath("//tbody/tr[3]/td/text()").extract()[0][5:14]
        content = ""
        for word in response.xpath("//tbody/tr[4]//font/text()").extract():
            content += word
        item['content'] = content
        att_url = []
        for iurl in response.xpath("//*[@href]/@href"):
            if iurl.extract().split('.')[-1] in ['doc' , 'pdf' , 'xls' , 'docx']:
                att_url.append(iurl)
        item['att_url'] = att_url
        img_url = []
        for img in response.xpath("//img/@src").extract():
            if img.split('.')[-1] != 'gif':
                img_url.append(img)
        item['img_url'] = img_url
        print(item)
        yield item