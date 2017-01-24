import re
import urllib.request
import time as t
from bs4 import BeautifulSoup

Ip_par = '(?:(?:1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.){3}(?:1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)\:\d+'
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'}
#定义一个IP网站url的列表
Web_Info = [
   #这里填写提供免费IP的网站URL
    'http://www.youdaili.net/Daili/http/'
]

#定义一个类
class Ip_getting:
    def __init__(self,info):
        self.Ip_par = Ip_par
        self.headers = headers
        self.web_index = info
        self.url_num = ''
    #定义一个函数，获取最新IP代理的URL页面
    def Get_last_index(self,url):
        Code_body = urllib.request.Request(url, headers=self.headers)
        Code_body = urllib.request.urlopen(Code_body).read().decode('utf-8')
        soup = BeautifulSoup(Code_body,'lxml')
        soup_body = soup.select('div.chunlist > ul > li > p > a')
        print('正在获取'+soup_body[0].get_text())
        self.url_num = soup_body[0].get('href').split('/')[-1].split('.')[0]
        return soup_body[0].get('href')

    #定义一个函数，从单个网页上所有IP
    def Get_ip_f(self,url):
        Code_body = urllib.request.Request(url,headers = self.headers)
        Code_body = urllib.request.urlopen(Code_body).read().decode('utf-8')
        Ip_from_web = re.findall(self.Ip_par,Code_body)
        #print(Ip_from_web)
        return Ip_from_web

    #在上面函数基础上，从连续的网页获取所有IP
    def Get_ip(self,url):
        IP_url = self.Get_last_index(url)
        Ip_All = self.Get_ip_f(IP_url)
        i = 1
        while True:
            i += 1
            url = IP_url.replace(self.url_num, self.url_num + '_' + str(i))
            try:
                Code_body = urllib.request.Request(url, headers=self.headers)
                Code_body = urllib.request.urlopen(Code_body).read().decode('utf-8')
                soup = BeautifulSoup(Code_body, 'lxml')
            except Exception as e:
                if e.code == 404:
                    break
            Ip_All += self.Get_ip_f(url)
        print('共获取 %d 个IP' % len(Ip_All))
        return Ip_All
    #依次从取出免费IP网站的URL，采集其IP
    def get_ip_url(self):
        # 定义一个储存IP的列表
        Ip_Info = []
        for i in self.web_index:
            Ip_Info += self.Get_ip(i)
        #利用集合去除重复的
        Ip_Info = set(Ip_Info)
        print('去重后得到 %d 个'% len(Ip_Info))
        return Ip_Info

    #定义一个函数，验证IP是否有效
    def Verify_ip(self,ip):
        proxy_support = urllib.request.ProxyHandler({'http':str(ip)})
        opener = urllib.request.build_opener(proxy_support)
        opener.addheaders = [('User-Agent',self.headers['User-Agent'])]
        urllib.request.install_opener(opener)
        try:
            Web_body = urllib.request.urlopen('http://www.whatismyip.com.tw/',timeout=1).read().decode('utf-8')
            Ip_pa = '(?:(?:1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)\.){3}(?:1\d\d|2[0-4]\d|25[0-5]|[1-9]\d|\d)(?:\:\d+){0,1}'
            Ip_from_web = re.findall(Ip_pa, Web_body)
            if Ip_from_web:
                if Ip_from_web[0] == str(ip).split(':')[0]:
                    print('已获得有效IP',ip)
                    return ip
        except Exception:
            pass

    #定义一个函数，封装所有的任务
    def output_ip(self):
        # 定义一个列表，装载通过验证的IP
        print('正在获取有效IP代理列表，这个过程可能需要数分钟，请耐心等待...')
        Ip_pass = []
        start = t.clock()
        for ip in self.get_ip_url():
            if self.Verify_ip(ip):
                Ip_pass.append(ip)
        end = t.clock()
        print('通过验证，其中共有 %d 个有效代理IP可以正常使用，分别是' % len(Ip_pass))
        print(Ip_pass)
        print('本次获取代理共用时%.3f秒，谢谢您的耐心等待...' % (end - start))
        return Ip_pass

if __name__ == '__main__':
    #获得一个类实例
    Ip_get = Ip_getting(Web_Info)
    start = t.clock()
    Ip_get.output_ip()
    end = t.clock()
    print('本次共运行%.3f秒' % (end-start))


