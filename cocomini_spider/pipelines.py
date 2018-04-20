# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

def trimNovel(str):
    #可抽取为工具类方法
    return str.replace('\r','').replace('\n','').replace('\t','').strip()
def trimChapter(str):
    #可抽取为工具类方法
    return str.replace('\r\n    \r\n        『章节错误,点此举报』\r\n    \r\n','').replace('\t\r\n\tapp2()\r\n    \r\n        『加入书签，方便阅读』\r\n    \r\n','').replace('\u3000\u3000','\\n')

class NovelPipeline(object):
    def process_item(self, item, spider):
        try:
            if "novel_img" in item:
                for i in range(0,len(item["novel_img"])):
                    #获取并提取数据
                    img = item["novel_img"][i]
                    title = item["novel_title"][i]
                    novel_type=trimNovel(item["novel_type"][i])
                    author = item["novel_author"][i].replace("作者：", "")
                    intro =trimNovel( item["novel_intro"][i])
                    # print("----------------------------小说内容----------------------------")
                    # print("图片:",img)
                    # print("书名:",title)
                    # print("作者:",author)
                    # print("简介:",intro)
                    # print("----------------------------小说内容----------------------------")
            return item
        except Exception as e:
            print("novelpipe:",e)


class ChapterPipeline(object):
    # 发送全部章节的请求,得到每一章节的地址.根据先对比redis,如果redis里面存在则不爬取,如果不存在再去数据库对比.
    # 如果都不存在.则爬取,如果存在则加入到redis里面的2号库
    # redis作用2,key为链接,value为章节内容,如果访问就把小说内容加入到非关系数据库(3号库)
    def process_item(self, item, spider):
        try:
            if "chapter_title" in item:
                for i in range(0,len(item["chapter_title"])):
                    sort = item["chapter_sort"]
                    title=item["chapter_title"][i]
                    content=trimChapter(item["chapter_content"][i])
                    if content.strip().startswith("正在手打中"):
                        content="源网站没有资源"
                    print("----------------------------章节内容----------------------------")
                    print("顺序:",sort)
                    print("标题:", title)
                    print("内容:", content)
                    print("----------------------------章节内容----------------------------")
            return item

        except Exception as e:
            print("chapterpipe:",e)

