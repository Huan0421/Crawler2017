import threading
import requests
from bs4 import BeautifulSoup
import queue
import random as r
import re
import  time as t



#

#此处填写cookie
cookie = 'BIGipServer=3664316938.20480.0000; PHPSESSID=hviau7oopjljmtvdvbq9ij1006; __utmt=1; __utmt_t2=1; domain=hz; __utma=1.2025871313.1487587209.1487587209.1487587209.1; __utmb=1.2.10.1487587209; __utmc=1; __utmz=1.1487587209.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utma=228451417.910947426.1487587209.1487587209.1487587209.1; __utmb=228451417.2.10.1487587209; __utmc=228451417; __utmz=228451417.1487587209.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_b3ad53a84ea4279d8124cc28d3c3220f=1487587209; Hm_lpvt_b3ad53a84ea4279d8124cc28d3c3220f=1487587214; _pzfxuvpc=1487587209398%7C1451989414343118036%7C2%7C1487587213959%7C1%7C%7C9960210840135672870; _pzfxsvpc=9960210840135672870%7C1487587209398%7C2%7C; Hm_lvt_b43bb26486d6ce24dcd04b25a379cc12=1487587209; Hm_lpvt_b43bb26486d6ce24dcd04b25a379cc12=1487587214; Hm_lvt_0bccd3f0d70c2d02eb727b5add099013=1487587209; Hm_lpvt_0bccd3f0d70c2d02eb727b5add099013=1487587214; _va_id=20b425669c4caf72.1487587209.1.1487587214.1487587209.; _va_ses=*'

#定义一个空代理列表
IP_pool=[]

class Producer(threading.Thread):
    def __init__(self,ipool,work_list):
        super().__init__()
        self.index_url = 'http://hz.5i5j.com'
        self.pages = 1
        self.ip_out = []
        self.work_list = work_list
        self.ipool = ipool
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 '
                                      '(KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                        'Cookie':cookie,}

    #定义一个函数获取网页链接
    def get_web(self,url):
        if self.ipool:
            ip = r.choice(self.ipool)
            ip = r'http://'+ip
            proxy = {'http':ip}
            web_data = requests.get(url, headers=self.header, proxies=proxy)
            web_data.encoding = 'utf-8'
            print('“我爱我家”生产者线程正在使用代理%s获取url' % proxy)
        else:
            web_data = requests.get(url, headers=self.header)
            web_data.encoding = 'utf-8'


        soup = BeautifulSoup(web_data.text,'lxml')
        info_list = soup.select('div.list-info')
        Ip_info = []
        for i in info_list:
            temp_list = []
            target_url = i.select('h2 > a')[0].get('href')
            temp_list.append(target_url)
            target_localtion = i.findAll('a',{'target':'_blank'})[-2].get_text()
            temp_list.append(target_localtion)
            Ip_info.append(temp_list)
            self.work_list.put(temp_list)
            #print('“我爱我家”生产者线程已将列表 %s 已写入队列' % str(temp_list))
        return Ip_info

    #定义一个函数验证页面是否有效
    def vertify(self,url):
        web_data = requests.get(url)
        soup = BeautifulSoup(web_data.text,'lxml')
        result = soup.select('h4.no-result')
        return result
        
    def run(self):
        print('“我爱我家”生产者线程开始启动')
        while True:
            url_now = self.index_url+r'/exchange/n'+str(self.pages)
            if self.vertify(url_now):
                break
            self.pages +=1
            self.ip_out += self.get_web(url_now)
            print('“我爱我家”生产者线程来到第%s页，目前共获取链接%s个' % (self.pages,len(self.ip_out)))

class Consumer(threading.Thread):
    def __init__(self, ipool, name,work_list):
        super().__init__()
        self.index_url = 'http://hz.5i5j.com'
        self.work_list = work_list
        self.ipool = ipool
        self.name = name
        self.header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                        'Cookie':cookie,}
    #定义一个函数从页面获取所需信息
    def get_info(self,info):
        url = self.index_url + info[0]
        if self.ipool:
            ip = r.choice(self.ipool)
            ip = r'http://'+ip
            proxy = {'http':ip}
            web_data = requests.get(url,headers=self.header,proxies=proxy)
        else:
            web_data = requests.get(url, headers=self.header)
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text,'lxml')

        #总价
        Price_total = soup.select('span.font-price')
        #单价
        Price_Unit_body = re.search(r'单价：</b>(\d+)',str(soup))
        Price_Unit = Price_Unit_body.group(1)
        #单位
        Price_Unit_unit = '元'
        #建筑面积
        area_total_body = re.search(r'建筑面积：</b>(\d+.\d+)', str(soup))
        area_total = area_total_body.group(1) if area_total_body else '暂无数据'
        #户型
        style_house_body = re.search(r'户型：</b>(.*[厅卫])', str(soup))
        style_house = style_house_body.group(1)
        # 定义一个字典储存数据
        data = {
            'Price_Unit': Price_Unit,
            'Price_Unit_unit': Price_Unit_unit,
            'Price_total': Price_total[0].get_text() if Price_total else '暂无数据',
            'area_total': area_total,
            'style_house': style_house if style_house else '暂无数据',
            'location_house': info[-1],
        }


    def run(self):
        print('“我爱我家”消费者线程 %s 启动' % self.name)
        while True:
            info = self.work_list.get()
            self.get_info(info)


def wawjia_main(ipool,num=1):
    work_list = queue.Queue()

    thread_producer = Producer(ipool,work_list)
    thread_producer.daemon = True
    thread_producer.start()

    for i in range(1,num+1):
        thread_consumer = Consumer(ipool,'“我爱我家'+str(i)+'号消费者',work_list)
        thread_consumer.daemon = True
        thread_consumer.start()

    while True:
        t.sleep(10)
        print('目前队列中共有数据 %s 条' % work_list.qsize())
        if work_list.qsize() == 0:
            print('“我爱我家”的主线程结束，准备进入下一个任务...')

if __name__ == '__main__':
    wawjia_main(IP_pool)
