import queue
import producer
import consumer
import time as t

#这里定义一个全局变量储存更新后的IP
IP_pool=[]

class consumer_Zs(consumer.Consumer):
    def __init__(self,work_queue,myname,ipool,cookie,home_url):
        super().__init__(work_queue,myname,ipool,cookie,home_url)

    def get_info(self,soup):
        U_price = soup.select('#spvprice')
        A_price = soup.select('#spPrice')
        style_a = soup.select('#spH_roomNum1')
        style_b = soup.select('#spH_hallNum1')
        style_c = soup.select('#spH_sanitationNum1')
        area = soup.select('#spH_building')
        loc = soup.select('div.est_rh_list21')
        data = {
            'U_price': U_price[0].get_text() if U_price else '暂无',
            'A_price': A_price[0].get_text() if A_price else '暂无',
            'style': (style_a[0].get_text() if style_a else '0')+'房'+(style_b[0].get_text() if style_b else '0')+'厅'+(style_c[0].get_text() if style_c else '0')+'卫',
            'area': area[0].get_text() if area else '暂无',
            'loc': [i for i in loc[0].stripped_strings] if loc else '暂无',
        }
        print(data)

def Zs_main(IP_pool,num=1):
    work_queue = queue.Queue()
    home_url = 'http://hz.hbhousing.com.cn'+'/'
    mycookie = ''


    thread_producer = producer.Producer(home_url+'HouseList.aspx?HTIE=1&PageNo=',mycookie,'“住商不动产”',8,'',work_queue,IP_pool,'a.houselist_link')
    thread_producer.daemon = True
    thread_producer.start()

    for i in range(1,num+1):
        thread_cosr = consumer_Zs(work_queue,'“住商不动产”'+str(i)+'号线程',IP_pool,mycookie,home_url)
        thread_cosr.daemon = True
        thread_cosr.start()

    while True:
        t.sleep(10)
        print('住商不动产队列大小' + str(work_queue.qsize()))

if __name__=='__main__':
    Zs_main(IP_pool)
