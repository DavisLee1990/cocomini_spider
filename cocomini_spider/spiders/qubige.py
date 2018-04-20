# -*- coding: utf-8 -*-
import scrapy
import requests
from cocomini_spider.items import NovelItem, ChapterItem
import os
from scrapy.http import Request
from urllib import parse
from lxml import etree


class QubigeSpider(scrapy.Spider):
    """本类是分类页面级爬取类,流程为小说地址爬取--->小说详情页爬取---->小说章节爬取--->小说内容爬取"""
    name = 'qubige'
    allowed_domains = ['m.xs.la']
    # start_urls = ['https://m.xs.la/newclass/0/1.html']

    def start_requests(self):
        #开始解析前发送一个请求
        url="https://m.xs.la/newclass/0/1.html"
        yield Request(url,callback=self.parse_novels)

    def parse_novels(self, response):
        #开始解析
        try:
            #一,把第一页的数据爬取下来.
            print(response.url)
            urls = response.xpath('//div[@class="hot_sale"]/a/@href').extract()
            print(urls)
            yield Request(url=parse.urljoin("https://m.xs.la", urls[0]), callback=self.parse_novel)#测试,只有第一本的数据爬取
            # for i in urls:
            #     yield Request(url=parse.urljoin("https://m.xs.la", i), callback=self.parse_novel)#把小说url交给parse_novel下载器处理
            # 二,如果页面爬取完毕就进入下一页爬取
            # next_page = response.xpath('//a[@id="nextPage"]/@href').extract()
            # print(next_page)
            # if next_page :
            #     #暂时只爬取到5页
            #     print(".....................跳转下一页面...........................")
            #     yield scrapy.Request(url=parse.urljoin("https://m.xs.la",next_page[0]), callback=self.parse)#递归下载
            # elif next_page[0].endwith("5.html"):
            #     return
        except Exception as e:
            print("主类报错:", e)

    def parse_novel(self, response):
        """此类是小说类,爬取小说的内容"""
        try:
            print("小说类返回页面:", response.url)
            # novelItem = NovelItem()
            # novelItem["novel_img"] = response.xpath('//div[@class="synopsisArea_detail"]/img/@src').extract()
            # novelItem["novel_title"] = response.xpath('//span[@class="title"]/text()').extract()
            # novelItem["novel_author"] = response.xpath('//div[@class="synopsisArea_detail"]//p[@class="author"]/text()').extract()
            # novelItem["novel_type"] = response.xpath('//div[@class="synopsisArea_detail"]/p[@class="sort"]/text()').extract()
            # novelItem["novel_intro"] = response.xpath('//div[@id="breview"]').xpath('string(.)').extract()
            # yield novelItem  # 把接受的对象交给pipelines中的NovelPipeline处理
            # 获取全部章节目录
            all_chapter_url = response.xpath('//a[@id="AllChapterList2"]/@href').extract()  # 全部章节链接
            print("全部章节连接:",all_chapter_url)
            '''
            url=parse.urljoin("https://m.xs.la",all_chapter_url[0])
            print(all_chapter_url[0])    得出来的地址是-->/248_248993/all.html
            print(url)  得出来的地址是-->https://m.xs.la/ /248_248993/all.html
            这里的urljoin出现一个小BUG,如上述所见.我们看到多了一条/.原因是all_chapter_url[0]的地址如:
            " /246_246383/all.html",前面是有一个空格的
            '''
            all_chapter_res = requests.get(url=parse.urljoin("https://m.xs.la", all_chapter_url[0].strip()))  # 访问全部章节页面
            all_chapter_res.encoding = 'utf-8'
            all_chapter_text = all_chapter_res.text
            tree = etree.HTML(all_chapter_text.encode("utf-8"))
            chapter_url = tree.xpath('//div[@id="chapterlist"]/p/a/@href')
            chapter_title = tree.xpath('//div[@id="chapterlist"]/p/a/text()')
            print("查看顺序:",chapter_title)
            # for i in range(1,len(chapter_url)):
            for i in range(1, 6):#测试只爬取5个章节
                # 注:从第一个开始,0是到达底部标签,所以不爬取.并且把title交给下一个解析器
                yield Request(url=parse.urljoin("https://m.xs.la", chapter_url[i]),meta={'sort':i,'chapter_title': chapter_title[i]},
                              callback=self.parse_chapter)  # 把小说url交给parse_novel下载器处理

        except Exception as e:
            print("小说类报错:", e)

    def parse_chapter(self, response):
        """此类是章节类,爬取每本小说的章节"""
        #注意,因为是异步请求的,res得到的顺序是不一样的,所以在meta里面加入循环变量i用于章节的排序
        try:
            chapterItem=ChapterItem()
            chapterItem["chapter_sort"] = [response.meta['sort']]
            chapterItem["chapter_title"] = [response.meta['chapter_title']]
            chapterItem["chapter_content"] = response.xpath('//div[@id="chaptercontent"]').xpath('string(.)').extract()
            if not chapterItem["chapter_content"][0]:
                #注意这里可能出现text为空的情况,意味着爬取失败,交给爬虫反复爬取
                yield Request(url=response.url,
                              meta={'sort': response.meta['sort'],'chapter_title': response.meta['chapter_title']},
                              callback=self.parse_chapter)
            yield chapterItem  # 把接受的对象交给pipelines中的ChapterPipeline处理
        except Exception as e:
            print("章节方法报错:",e)

