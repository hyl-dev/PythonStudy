import requests
import time
from bs4 import BeautifulSoup
import re
import pymongo

client = pymongo.MongoClient('192.168.31.234',27017)
info_zhuan = client['info_zhuan']
data_zz = info_zhuan['data_zz']

def get_links_from(page):
    urls = []
    list_view = 'http://bj.58.com/pbdn/0/pn{}'.format(str(page))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    for link in soup.select('td.t a.t'):
        link_url = link.get('href').split('?')[0]
        # delete the jump url
        if 'http://jump.zhineng.58.com' in link_url:
            continue
        urls.append(link_url)
    return urls

def get_detail_data( start_page , end_page):
    for one in range( start_page , end_page ):
        raw_urls = get_links_from(one)
        for url in raw_urls:
            web_data = requests.get( url )
            web_data.encoding = "utf-8"
            soup = BeautifulSoup(web_data.text, "lxml")
            view_p = soup.select('span.look_time')[0].text
            want_person = soup.select('span.want_person')[0].text
            price_orie = soup.select('b.price_ori')[0].text if len(soup.find_all('b', 'price_ori')) > 0 else None
            data={
                "titile":[soup.select('h1.info_titile')[0].text],
                "price_now":[soup.select('span.price_now > i')[0].text],
                "price_ori":[ re.sub("\D","",price_orie) if price_orie is not None else None  ],
                "area":[soup.select('div.palce_li > span > i')[0].text],
                "tag":[soup.select('div.biaoqian_li')[0].text.replace('\n','')],
                "views":[re.sub("\D","",view_p)],
                "wants":[re.sub('\D','',want_person)]
            }
            time.sleep(1)
            #data_zz.insert_one(data)
            print(data)


def get_datas():
    start_page=int(input("input the start page:"))
    print("please press “enter”")
    end_page=int(input("input end page："))
    print("please press “enter”")
    get_detail_data(start_page, end_page)

if __name__ == '__main__':
    get_datas()
