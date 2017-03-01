import Ip_Get_class
import threading
from baby_lianjia import lianjia_main
from baby_wawjia import wawjia_main
from baby_hshb import hsfb_main
from baby_dsfw import dsfw_info,dsfw_urls
from baby_Qfw import Q_main
from baby_kwgj import KW_main
from baby_zsbdc import Zs_main
import time as t

#这里定义一个全局变量储存更新后的IP
IP_pool=[]
#这里填写提供免费IP的网站URL
Web_Info = ['http://www.youdaili.net/Daili/http/']
#获取ip代理池的线程类对象
class IP_GET(threading.Thread):
    def __init__(self):
        super().__init__()
    def run(self):
        print('IP获取线程开始启动')
        global IP_pool
        while True:
            print('IP池开始更新')
            IP_pool = Ip_Get_class.output_ip(4)
            print('IP池完成了一次更新')

#定义一个函数，创建一个获取IP的线程
def get_iplist():
    thread_ip = IP_GET()
    thread_ip.daemon = True
    thread_ip.start()

get_iplist()


#链家地产数据
lianjia_main('链家西湖','xihu',59,IP_pool,4)
lianjia_main('链家下城','xiacheng',41,IP_pool,2)
lianjia_main('链家江干','jianggan',56,IP_pool,2)
lianjia_main('链家拱墅','gongshu',37,IP_pool,2)
lianjia_main('链家上城','shangcheng',26,IP_pool,2)
lianjia_main('链家滨江','bingjiang',29,IP_pool,2)
lianjia_main('链家余杭','yuhang',47,IP_pool,2)
lianjia_main('链家萧山','xiaoshan',21,IP_pool,2)
print('“链家”数据处理完毕')

#我爱我家地产数据
wawjia_main(IP_pool)
print('“我爱我家”数据处理完毕！')

#豪世华邦数据
hsfb_main(IP_pool)
print('“豪世华邦”数据处理完毕！')

#都市房网数据
dsfw_info(dsfw_urls[0])
dsfw_info(dsfw_urls[1])
print('“都市房网”数据处理完毕！')

#Q房网数据
Q_main(IP_pool)
print('“房网”数据处理完毕！')

#科威国际数据
KW_main(IP_pool)
print('“科威国际”数据处理完毕！')

#住商数据
Zs_main(IP_pool)
print('“住商不动产”数据处理完毕！')