from bs4 import BeautifulSoup
import time as t
import requests
import threading
import random as r

#定义一个线程，专门用于生产可用的URL，并写入队列
class Producer(threading.Thread):
    #初始化
    def __init__(self,home_url,mycookie,myname,page_all,page_url,work_queue,ipool,url_path):
        super().__init__()
        # 设置主页地址
        self.url_index = home_url
        #设置cookie
        self.cookie = mycookie
        #设置爬虫名称
        self.myname = myname
        # 设置链接总页数
        self.page_all = page_all
        #页码标记参数
        self.page_url = page_url
        #设置工作队列
        self.work_queue = work_queue
        #设置IP代理池
        self.ipool = ipool
        #设置链接所在路径
        self.url_path = url_path
        #设置链接路径
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
                        'Cookie':self.cookie}

    #线程主体
    #定义一个函数从指定URL的页面获取链接,并写入队列
    def get_url_home(self,url):
        #定义一个列表用于装载url
        Url_Info=[]
        #设置代理
        if self.ipool:
            try:
                ip = r.choice(self.ipool)
                ip = r'http://'+ip
                proxies = {'http':ip}
                print(self.myname+'生产者线程正在使用代理IP %s ' % ip)
                web_data = requests.get(url, headers=self.headers, proxies=proxies, timeout=3)
            except Exception as e:
                print('由于'+str(e)+'原因，重新启动！')
                self.get_url_home(url)
        else:
            web_data = requests.get(url,headers = self.headers,timeout=3)
        web_data.encoding = 'utf-8'
        soup = BeautifulSoup(web_data.text,'lxml')
        url_got = soup.select(self.url_path)
        for i in url_got:
            # 将URL写入队列
            self.work_queue.put(i.get('href'))
            #print(i.get('href'))
            Url_Info.append(i.get('href'))

        return Url_Info

    #在上面函数的基础上定义一个函数从首页获取链接
    def run(self):
        print(self.myname+'生产者线程开始启动')
        Url_All = []
        start = t.clock()
        for i in range(1,self.page_all+1):
            page_url = self.url_index +self.page_url+str(i)
            print(self.myname+'生产者线程正在使用'+str(page_url)+'访问网站！')
            Url_All += self.get_url_home(page_url)
            print(self.myname+'生产者线程已将链接写入队列')
            t.sleep(1)
        end = t.clock()
        print(self.myname+'生产者线程共获得链接 %s 条,共运行了 %.3f 秒' % (len(Url_All),(end-start)))
        return Url_All