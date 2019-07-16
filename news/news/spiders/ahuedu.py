# -*- coding: utf-8 -*-
import scrapy
from ..items import NewsItem
from lxml import etree

class AhueduSpider(scrapy.Spider):
    name = 'ahuedu'
    #allowed_domains = ['www.ahu.edu.cn']
    start_urls = ['http://www.ahu.edu.cn/']

    def parse(self , response):
        news = response.xpath("//*[@frag='窗口5' or @frag='窗口6' or @frag='窗口12' \
            or @frag='窗口14' or @frag='窗口102' or @frag='窗口103' or @frag='窗口104'  \
                or @frag='窗口105' or @frag='窗口106' or @frag='窗口107' or @frag='窗口108'  \
                    or @frag='窗口109' or @frag='窗口172' or @frag='窗口288']//*[@class='news_title']/a")
        for new in news:
            content_url = new.xpath("./@href").extract()[0]
            yield scrapy.Request("http://www.ahu.edu.cn" + content_url , callback = self.parse_content)

    def parse_content(self , response):
        item = NewsItem()
        item['title'] = response.xpath("//h1[@class='arti-title']/text()").extract()[0]
        item['datetime'] = response.xpath("//span[@class='arti-update']/text()").extract()[0].replace("发布时间：","")
        content = ""
        for word in response.xpath("//article[@class = 'read']//span/text()").extract():
            content = content + word
        item['content'] = content
        img_urls = []
        if len(response.xpath("//p[@style='text-align:center;']/img/@src")):
            img_urls.append(response.xpath("//p[@style='text-align:center;']/img/@src").extract()[0])
        item['img_url'] = img_urls

        attrs = []
        if len(response.xpath("//a[@sudyfile-attr]/@href")):
            attrs.append(response.xpath("//a[@sudyfile-attr]/@href").extract()[0])
        item['att_url'] = attrs
        yield item
        #print(item)