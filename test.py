import time as t
import queue
import producer



#这里定义一个全局变量储存更新后的IP
IP_pool=[]
home_url = 'http://hz.hshb.cn/chushou'
mycookie = 'jsid=e8d5f2d4-efab-4d79-84a9-756b19543b92; Hm_lvt_c657266d252fd02531ca2079661b96c0=1488071604; Hm_lpvt_c657266d252fd02531ca2079661b96c0=1488073746'
work_queue = queue.Queue()
m = producer.Producer(home_url,mycookie,'豪世华邦',10,'lg',work_queue,IP_pool,'div.mhName > a')
m.start()
while True:
    t.sleep(10)
    print('队列大小'+str(work_queue.qsize()))