import queue
import producer
import consumer
import time as t

#这里定义一个全局变量储存更新后的IP
IP_pool=[]

class consumer_hshb(consumer.Consumer):
    def __init__(self,work_queue,myname,ipool,cookie,home_url):
        super().__init__(work_queue,myname,ipool,cookie,home_url)

    def get_info(self,soup):
        U_price = soup.select('div.info > span')
        A_price = soup.select('div.zonJia > span')
        style = soup.select('div.threPer > span')
        area = soup.select('div.threPer > span')
        loc = soup.select('p.spTxt > a')
        data = {
            'U_price': U_price[0].get_text() if U_price else '暂无',
            'A_price': A_price[0].get_text() if A_price else '暂无',
            'style': style[0].get_text() if style else '暂无',
            'area': area[-1].get_text() if area else '暂无',
            'loc': loc[-1].get_text() if loc else '暂无',
        }
        print(data)

def hsfb_main(IP_pool,num=1):
    work_queue = queue.Queue()
    home_url = 'http://hz.hshb.cn'
    mycookie = 'jsid=e8d5f2d4-efab-4d79-84a9-756b19543b92; Hm_lvt_c657266d252fd02531ca2079661b96c0=1488071604; Hm_lpvt_c657266d252fd02531ca2079661b96c0=1488073746'


    thread_producer = producer.Producer(home_url+'/chushou',mycookie,'“豪世华邦”',10,'/lg',work_queue,IP_pool,'div.mhName > a')
    thread_producer.daemon = True
    thread_producer.start()

    for i in range(1,num+1):
        thread_cosr = consumer_hshb(work_queue,'“豪世华邦”'+str(i)+'号线程',IP_pool,mycookie,home_url)
        thread_cosr.daemon = True
        thread_cosr.start()

    while True:
        t.sleep(10)
        print('豪世华邦队列大小' + str(work_queue.qsize()))


if __name__ == '__main__':
    hsfb_main(2)


