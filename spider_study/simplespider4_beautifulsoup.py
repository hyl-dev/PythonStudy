#!/usr/bin/python3
# -*- coding:utf-8 -*-
from bs4 import BeautifulSoup
import requests
import pymongo

client = pymongo.MongoClient('192.168.31.234',27017)
info = client['info']
data_tab = info['data_tab']

def get_links_from(page):
    urls = []
    list_view = 'http://bj.58.com/pbdn/1/pn{}'.format(str(page))
    wb_data = requests.get(list_view)
    soup = BeautifulSoup(wb_data.text, 'lxml')

    for link in soup.select('td.t a.t'):
        link_url = link.get('href').split('?')[0]
        # delete the jump url
        if 'http://jump.zhineng.58.com' in link_url:
            continue
        urls.append(link_url)
    return urls


def get_views_from(url):
    info_id = url.split('/')[-1].strip('x.shtml')
    api = 'http://jst1.58.com/counter?infoid={}'.format(info_id)
    # need add the js header ,or it can't read the views count
    headers = {
        'Accept': '*/*',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'Language:zh-CN,zh;q=0.8',
        'Cache-Control': 'max-age=0',
        'Connection': 'keep-alive',
        'Cookie': 'bj58_id58s="RXp5VkR1M21tM0tVMzc5OQ=="; id58=c5/njVd1wDpW16ToCtyxAg==; als=0; city=bj; 58home=bj; ipcity=cc%7C%u957F%u6625%7C0; sessionid=7d7a05c7-566c-4ee8-9a33-f9491ffc295f; __utma=253535702.545205630.1467371246.1467371246.1467371246.1; __utmc=253535702; __utmz=253535702.1467371246.1.1.utmcsr=bj.58.com|utmccn=(referral)|utmcmd=referral|utmcct=/pbdn/1/; myfeet_tooltip=end; 58tj_uuid=7dc55421-36df-4bfa-a534-0f7dd003862d; new_session=0; new_uv=3; utm_source=; spm=; init_refer=; final_history={}%2C26342559128371; bj58_new_session=0; bj58_init_refer=""; bj58_new_uv=3'.format(
            str(info_id)),
        'Host': 'jst1.58.com',
        'Referer': 'http://bj.58.com/pingbandiannao/{}x.shtml'.format(info_id),
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    }
    wb_data = requests.get(api, headers=headers)
    if wb_data.status_code == 200:
        views = wb_data.text.split('=')[-1]
        return views
    return 0


def get_item_info(start_page, end_page):
    for one in range(start_page, end_page):
        urls = get_links_from(one)
        for url in urls:
            wb_data = requests.get(url)
            soup = BeautifulSoup(wb_data.text, 'lxml')
            data = {
                'title': soup.title.text,
                'price': soup.select('.price')[0].text if len(soup.find_all('span', 'price')) > 0 else 0,
                'area': list(soup.select('.c_25d')[0].stripped_strings) if soup.find_all('span', 'c_25d') else None,
                'date': soup.select('.time')[0].text,
                'views': get_views_from(url)
            }
            data_tab.insert_one(data)

if __name__ == '__main__':
    get_item_info(1, 5)
