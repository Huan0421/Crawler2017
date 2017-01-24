import urllib.request
from bs4 import BeautifulSoup
import time as t
import re
import requests
import threading
import queue
import random as r
#配置路径
import os
import sys
sys.path.append(os.curdir)
import Ip_Get_class

#要爬取的网站首页URL
url_index = 'http://hz.lianjia.com/ershoufang/'

#这里定义一个全局变量储存更新后的IP
IP_pool=[]

#定义一个线程，专门用于生产可用的URL，并写入队列
class Producer(threading.Thread):
    #初始化
    def __init__(self,url,page_all,work_queue):
        super().__init__()
        self.work_queue = work_queue
        self.page_all = page_all
        self.url_index = url
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    #线程主体
    #定义一个函数从指定URL的页面获取链接,并写入队列
    def get_url_from_web(self,url):
        #定义一个列表用于装载
        url_get_info=[]
        #设置代理
        if IP_pool:
            ip = r.choice(IP_pool)
            ip = 'http://'+ip
            proxies = {'http':ip}
            print('线程1正在使用代理IP %s' % ip)
            web_data = requests.get(url, headers=self.headers, proxies=proxies, timeout=3)
        else:
            web_data = requests.get(url,headers = self.headers,timeout=3)
        soup = BeautifulSoup(web_data.text,'lxml')
        url_got = soup.select('div.title > a')

        for i in url_got:
            # 将URL写入队列
            self.work_queue.put(i.get('href'))
            url_get_info.append(i.get('href'))

        return url_get_info
    #在上面函数的基础上定义一个函数从首页获取链接
    def run(self):
        print('线程1启动')
        Url_All = []
        start = t.clock()
        for i in range(1,self.page_all+1):
            page_url = self.url_index + 'pg%s/' % str(i)
            Url_All += self.get_url_from_web(page_url)
            print('线程1的链接已写入队列')
        end = t.clock()
        print('共获得链接 %s 条' % len(Url_All))
        print('共运行了 %.3f 秒' % (end-start))
        return Url_All

#再定义一个线程，从对列中取出链接并采集信息
class house_info(threading.Thread):
    #初始化参数
    def __init__(self,work_queue,name):
        super().__init__()
        self.work_queue = work_queue
        self.name = name
        self.headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
    #定义一个函数，从指定的页面获取详情信息
    def run(self):
        Info_all = []
        print('线程 %s 启动' % self.name)
        while True:
            url = self.work_queue.get()
            # 设置代理
            while True:
                try:
                    if IP_pool:
                        ip = r.choice(IP_pool)
                        ip = 'http://' + ip
                        proxies = {'http': ip}
                        print('线程 %s 正在使用代理IP %s' % (ip,self.name))
                        web_data = requests.get(url, headers=self.headers, proxies=proxies, timeout=3)
                    else:
                        web_data = requests.get(url, headers=self.headers, timeout=3)
                    break
                except Exception as e:
                    print(e)

            soup = BeautifulSoup(web_data.text, 'lxml')
            Unit_P = soup.select('div.unitPrice > span')
            if Unit_P:
                Unit_P = re.search(r'unitPriceValue">(\d+?)<i>(.*?)</i>',str(Unit_P[0]))
                #房单位价格
                Price_Unit = Unit_P.group(1)
                #单位价格所用单位
                Price_Unit_unit = Unit_P.group(2)
            else:
                Price_Unit = Price_Unit_unit = '暂无数据'
            #总房价
            Price_total = soup.select('div.price > span.total')
            #总面积
            area_total = soup.select('div.area > div.mainInfo')
            #户型
            style_house = soup.select('div.room > div.mainInfo')
            #位置
            location_house = soup.select('div.areaName > span.info')
            #定义一个字典储存数据
            data={
                'Price_Unit':Price_Unit,
                'Price_Unit_unit':Price_Unit_unit,
                'Price_total':Price_total[0].get_text() if Price_total else '暂无数据',
                'area_total':area_total[0].get_text() if area_total else '暂无数据',
                'style_house':style_house[0].get_text() if style_house else '暂无数据',
                'location_house':location_house[0].stripped_strings if location_house else '暂无数据',
            }
            print('线程 %s 运行中，已成功获取数据' % self.name)
            Info_all.append(data)
            t.sleep(1)
        return Info_all

class IP_GET(threading.Thread):
    def __init__(self,info):
        super().__init__()
        self.info = info
    def run(self):
        print('线程3开始启动')
        global IP_pool
        while True:
            print('IP池开始更新')
            ip_get = Ip_Get_class.Ip_getting(self.info)
            IP_pool = ip_get.output_ip()
            print('IP池完成了一次更新')

def main():
    work_queue = queue.Queue()
    thread_first = Producer(url_index,100,work_queue)
    thread_first.daemon = True  # 当主线程退出时子线程也退出
    thread_first.start()

    thread_a = house_info(work_queue,'a')
    thread_a.daemon = True  # 当主线程退出时子线程也退出
    thread_a.start()

    thread_b = house_info(work_queue, 'b')
    thread_b.daemon = True  # 当主线程退出时子线程也退出
    thread_b.start()

    thread_ip = IP_GET(Web_Info)
    thread_ip.daemon = True
    thread_ip.start()
    # 每十秒显示一下队列里的大小
    while True:
        print('目前队列中共有 %d 个链接' % work_queue.qsize())
        t.sleep(10)
    work_queue.join()  # 主线程会停在这里，直到所有数字被get()，并且task_done()

#这里填写提供免费IP的网站URL
Web_Info = ['http://www.youdaili.net/Daili/http/']

if __name__ == '__main__':
    main()




