#爬取豆瓣top250电影榜单

import requests
from lxml import etree

def GetText(url,headers):
    try:
        r = requests.get(url,headers = headers)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return "获取页面异常" 

if __name__ == '__main__':
    baseUrl = "https://movie.douban.com/top250"
    headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'}
    with open('top250.txt','w',encoding='utf-8') as f:
        for i in range(10):
            start = 25*i
            Url = "https://movie.douban.com/top250?start=" + str(start)
            contentUrls = etree.HTML(GetText(Url,headers)).xpath("//div[@class='hd']/a/@href")
            for url in contentUrls:
                content = etree.HTML(requests.get(url).text)
                rank = content.xpath("//*[@id='content']/div[1]/span[1]/text()")[0]
                title = content.xpath("//h1/span[1]/text()")[0]
                print(title)
                director = content.xpath("//*[@id='info']/span[1]/span[2]/a/text()")[0]
                types = []
                for type0 in content.xpath("//*[@property='v:genre']/text()"):
                    types.append(type0)
                rating_num = content.xpath("//*[@class='ll rating_num']/text()")[0]
                f.write(rank + ' ')
                f.write(title + ':' + '\n\t')
                f.write('rating_num:' + rating_num + '\n\t')
                f.write('director:' + director + '\n\t')
                f.write('type:')
                for type0 in types:
                    f.write(type0 + ',')
                f.write('\n')
