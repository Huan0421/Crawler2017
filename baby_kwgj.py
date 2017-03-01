import queue
import consumer
import time as t

#这里定义一个全局变量储存更新后的IP
IP_pool=[]





class consumer_KWGJ(consumer.Consumer):
    def __init__(self,work_queue,myname,ipool,cookie,home_url):
        super().__init__(work_queue,myname,ipool,cookie,home_url)

    def get_info(self,soup):
        info_list = soup.select('#estListC > ul > li')
        for i in info_list:
            A_price = i.select('div.est_rh_list27')
            style = i.select('div.est_rh_list24')
            area = i.select('div.est_rh_list25')
            loc = i.select('div.est_rh_list21')
            data = {
                'U_price': '暂无',
                'A_price': A_price[0].get_text() if A_price else '暂无',
                'style': style[0].get_text() if style else '暂无',
                'area': area[0].get_text() if area else '暂无',
                'loc': loc[0].get_text() if loc else '暂无',
            }
            print(data)

def KW_main(IP_pool,num=1):
    work_queue = queue.Queue()

    for i in range(1,1168):
        url = '/EstList/2?pageindex='+str(i)+'&p=571%2C%2C%2C%2C%2C%2C%2C'
        work_queue.put(url)

    home_url = 'http://www.cbzj.net'
    mycookie = 'AJSTAT_ok_pages=1; AJSTAT_ok_times=2'

    for i in range(1,num+1):
        thread_cosr = consumer_KWGJ(work_queue,'“科威国际”'+str(i)+'号线程',IP_pool,mycookie,home_url)
        thread_cosr.daemon = True
        thread_cosr.start()

    while True:
        t.sleep(10)
        print('科威国际队列大小' + str(work_queue.qsize()))

