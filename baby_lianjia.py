import time as t
import queue
import producer
import consumer
import pymysql

#这里定义一个全局变量储存更新后的IP
IP_pool=[]

db = pymysql.connect(
    host = 'localhost',
    port = 3306,
    user = 'wenhuan',
    password = 'wen8825994',
    db = 'rents',
    charset = 'utf8'
)

cursor = db.cursor()
#再定义一个线程，从对列中取出链接并采集信息
class Consumer_lianjia(consumer.Consumer):
    #初始化参数
    def __init__(self,work_queue, myname, ipool,cookie,home_url):
        super().__init__(work_queue, myname, ipool,cookie,home_url)

    #重写获取详情信息
    def get_info(self,soup):

        U_price = soup.select('li.short')
        A_price = soup.select('p.red.big > span')
        style = soup.select('p.red.big')
        area = soup.select('p.red.big')
        loc = soup.select(' ul > li.short')


        data = {
            'U_price':U_price[0].get_text() if U_price else '暂无',
            'A_price':A_price[0].get_text() if A_price else '暂无',
            'style':style[1].get_text() if style else '暂无',
            'area':area[-1].get_text() if area else '暂无',
            'loc':[i for i in loc[-1].stripped_strings][-1] if loc else '暂无',
        }

        #设置SQL语句
        sql = "INSERT INTO 链家数据(U_price,A_price,style,area,loc) VALUES ('%s','%s','%s','%s','%s')" % (
        str(data['U_price']), str(data['A_price']), str(data['style']), str(data['area']), str(data['loc']))
        cursor.execute(sql)
        db.commit()
            


        #print(data)







def lianjia_main(myname,url_add,page_all,ipool,num=1):
    cookie = 'lianjia_uuid=f61c0b10-36a1-45fc-b7c0-fdaa94ac94c9; _jzqy=1.1482665679.1482749358.1.jzqsr=baidu|jzqct=%E9%93%BE%E5%AE%B6%E7%BD%91.-; select_city=330100; _jzqckmp=1; _jzqx=1.1482676781.1488084009.6.jzqsr=hz%2Elianjia%2Ecom|jzqct=/ershoufang/.jzqsr=hz%2Elianjia%2Ecom|jzqct=/ershoufang/103100892775%2Ehtml; sample_traffic_test=test_61; select_nation=1; lj-ss=9fc6cee08e4d99ced4584517044e1242; _smt_uid=585faece.1543d313; _jzqa=1.1674168722816258300.1482665679.1488084009.1488085536.15; _jzqc=1; _gat_past=1; _ga=GA1.2.687775521.1482665685; CNZZDATA1254525948=638462224-1488082134-null%7C1488087534; CNZZDATA1253491255=1663134154-1488083351-null%7C1488091265; lianjia_ssid=06d54fbb-c171-4686-9e8b-e2d241f4a0d6'
    index_url = 'https://m.lianjia.com'

    work_queue = queue.Queue()
    thread_producer = producer.Producer(index_url+r'/hz/ershoufang/'+url_add, cookie, myname, page_all, '/pg', work_queue, IP_pool, 'li.pictext > a')
    thread_producer.daemon = True  # 当主线程退出时子线程也退出
    thread_producer.start()

    for i in range(1,num+1):
        thread_cosr = Consumer_lianjia(work_queue,myname+str(i)+'号消费者',ipool,cookie,index_url)
        thread_cosr.daemon = True  # 当主线程退出时子线程也退出
        thread_cosr.start()

    # 每十秒显示一下队列里的大小
    while True:
        t.sleep(10)
        print(myname+'队列中共有 %d 个链接' % work_queue.qsize())
        if work_queue.qsize() == 0:
            print(myname+'中的链接全部处理完毕，准备进入下一个任务...')
            db.close()
            break

    #work_queue.join()  # 主线程会停在这里，直到所有数字被get()，并且task_done()



if __name__ == '__main__':
    lianjia_main('链家西湖','xihu',59,IP_pool,2)

    #url_index = 'http://hz.lianjia.com/ershoufang/'
    #lianjia_main(url_index,100)



