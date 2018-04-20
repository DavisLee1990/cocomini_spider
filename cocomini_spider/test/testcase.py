# -*- coding:utf-8 -*-
#Author:Davis
# import redis
# r0=redis.Redis(host="101.132.110.217",port=6379,db=0)
# r1=redis.Redis(host="localhost",port=6379,db=1)
# print(r0.get("foo").decode())
# r0.set("pwd","love")
# print(r0.get("pwd").decode())
# r_pool=redis.ConnectionPool(host="localhost",port=6379,db=0)
# re0=redis.Redis(connection_pool=r_pool)
# re0.set("pwd","love")
# print(re0.get("pwd").decode())
# import  requests
# http =requests.get(url="http://www.iqiyi.com/")     #发送http请求
# print(type(http))
# for i in range(0,1):
#     print(i)
# from urllib import parse
# urls=["/247_247193/all.html"]
# test=parse.urljoin("https://m.xs.la",urls[0])
# print(test)
import operator
list=[[1,"zhansan",22],[4,"lisi",18],[2,"qianwu",25],[3,"heihei",30]]
list.sort(key=operator.itemgetter(2))
print(list)