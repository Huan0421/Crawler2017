from bs4 import BeautifulSoup
import time as t
import requests
import threading
import random as r


# 再定义一个线程，从对列中取出链接并采集信息
class Consumer(threading.Thread):
    # 初始化参数
    def __init__(self,work_queue,myname,ipool,cookie,home_url):
        super().__init__()
        self.work_queue = work_queue
        self.myname = myname
        self.ipool = ipool
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
            'Cookie': cookie}
        self.home_url = home_url

    # 定义一个函数，从指定的页面获取详情信息
    def get_info(self, soup):
        pass

    def run(self):
        Info_all = []
        print(self.myname + '消费者启动')
        while True:
            #获取锁，用于线程同步
            threadLock.acquire()
            url = self.work_queue.get()
            #释放锁
            threadLock.release()
            url = self.home_url + url
           # print(url)
            # 设置代理
            while True:
                try:
                    if self.ipool:
                        ip = r.choice(self.ipool)
                        ip = 'http://' + ip
                        proxy = {'http': ip}
                        print(self.myname + '消费者正使用 %s' % (ip, self.name))
                        web_data = requests.get(url, headers=self.headers, proxies=proxy, timeout=3)
                    else:
                        web_data = requests.get(url, headers=self.headers, timeout=3)
                    break
                except Exception as e:
                    print('由于'+str(e)+'原因,消费者重启！')
            web_data.encoding = 'utf-8'
            soup = BeautifulSoup(web_data.text, 'lxml')
            self.get_info(soup)
            t.sleep(1)

threadLock = threading.Lock()