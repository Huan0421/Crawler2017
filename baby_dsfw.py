import requests
from bs4 import BeautifulSoup


dsfw_urls=['http://www.cncityhouse.com/csfy.asp?cxqy=&zdzj=&zgzj=&zsmj=&zdmj=&cxhx=&cxkey=&pxxm=djsj+desc+&ym=1&cxbm=0&x=26&y=12','http://www.cncityhouse.com/csfy.asp?cxbm=0&ym=2&cxqy=&zdzj=&zgzj=&cxhx=&cxkey=']

def dsfw_info(url):
    web_data = requests.get(url)
    web_data.encoding = 'gb2312'
    soup = BeautifulSoup(web_data.text,'lxml')
    info_list = soup.select('tr.words2 ')
    for i in info_list[:-2]:
        info=i.select('td')
        data={
            'A_price': info[5].get_text(),
            'U_price':info[4].get_text(),
            'area':info[3].get_text(),
            'style':info[2].get_text(),
            'loc':info[0].get_text(),
        }


