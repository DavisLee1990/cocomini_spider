# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NovelItem(scrapy.Item):
    '''本类是小说类'''
    novel_img = scrapy.Field()  # 封面
    novel_title = scrapy.Field()  # 书名
    novel_author = scrapy.Field()  # 作者
    novel_type = scrapy.Field()  # 类型
    novel_intro = scrapy.Field()  # 介绍


class ChapterItem(scrapy.Item):
    '''本类是章节类'''
    chapter_sort = scrapy.Field() #章节的顺序
    chapter_title = scrapy.Field() #章节标题
    chapter_content = scrapy.Field() #章节内容
