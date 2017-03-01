import queue
import producer
import consumer
import time as t

#这里定义一个全局变量储存更新后的IP
IP_pool=[]

class consumer_Qfw(consumer.Consumer):
    def __init__(self,work_queue,myname,ipool,cookie,home_url):
        super().__init__(work_queue,myname,ipool,cookie,home_url)

    def get_info(self,soup):
        U_price = soup.select('span.average-price')
        A_price = soup.select('p.head-info-price > span')
        style = soup.select('div.house-model > ul > li > p')
        area = soup.select('div.house-model > ul > li > p')
        loc = soup.select('li > p.fl.clearfix')
        data = {
            'U_price': U_price[0].get_text() if U_price else '暂无',
            'A_price': A_price[0].get_text() if A_price else '暂无',
            'style': style[0].get_text() if style else '暂无',
            'area': area[1].get_text() if area else '暂无',
            'loc': [i for i in loc[0].stripped_strings] if loc else '暂无',
        }
        print(data)

def Q_main(IP_pool,num=1):
    work_queue = queue.Queue()
    home_url = 'http://hangzhou.qfang.com'
    mycookie = 'qchatid=3286e9db-f04c-4244-8595-a9bf228b78df; _jzqy=1.1488071533.1488071533.1.jzqsr=baidu|jzqct=%E8%B1%AA%E4%B8%96%E5%8D%8E%E9%82%A6%E4%BA%8C%E6%89%8B%E6%88%BF.-; JSESSIONID=aaaJT60BPQRuW8k00p-Pv; cookieId=80c9580e-3fc6-4204-95a3-98d3ca1e45e7; _dc_gtm_UA-47416713-1=1; sid=358d5c13-9fe0-4082-9c79-433d723659ad; _ga=GA1.3.24579389.1488193538; Hm_lvt_de678bd934b065f76f05705d4e7b662c=1488071533,1488193538; Hm_lpvt_de678bd934b065f76f05705d4e7b662c=1488193588; _jzqa=1.2733468353717963300.1488071533.1488071533.1488193588.2; _jzqc=1; _jzqckmp=1; _jzqb=1.1.10.1488193588.1'


    thread_producer = producer.Producer(home_url+'/sale',mycookie,'“Q房网”',241,'/f',work_queue,IP_pool,'p.house-title > a')
    thread_producer.daemon = True
    thread_producer.start()

    for i in range(1,num+1):
        thread_cosr = consumer_Qfw(work_queue,'“Q房网”'+str(i)+'号线程',IP_pool,mycookie,home_url)
        thread_cosr.daemon = True
        thread_cosr.start()

    while True:
        t.sleep(10)
        print('Q房网队列大小' + str(work_queue.qsize()))

if __name__=='__main__':
    Q_main(IP_pool)
