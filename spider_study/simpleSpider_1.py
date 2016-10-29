#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import re
import xlwt3

row0 = [u'电影名称',u'别名',u'年份',u'评分',u'评价人数'] 
base_url = 'https://movie.douban.com/top250'

def get_url(page_num):
    if page_num == 0:
        url = base_url
    else:
        url = 'https://movie.douban.com/top250?start=' + str(25*page_num) + '&filter='
    return url


def get_html(url):
    r = urllib.request.urlopen(url)
    return r.read().decode('utf8','ignore')

def get_info(content):
    pattern = re.compile('<span class="title">(.*?)</span>.*?'
                         '<span class=.*?>&nbsp;/&nbsp;(.*?)</span>.*?'
                         '(\d\d\d\d).*?'
                         '<span class="rating_num" property="v:average">(.*?)</span>.*?'
                         '<span>(.*?)人评价</span>.*?', re.S)
    info = re.findall(pattern, content)
    return info

def write_info(infos, i,test):
    for info in infos:
        test.write(i, 0, info[0])
        test.write(i, 1, info[1].replace('&#39;', "'"))
        test.write(i, 2, info[2])
        test.write(i, 3, info[3])
        test.write(i, 4, info[4])
        i += 1
		
def save_file(f,test):
	style = 'pattern: pattern solid, fore_colour yellow; '
	style += 'font: bold on; ' 
	style += 'align: horz centre, vert center; '
	header_style = xlwt3.easyxf(style) 
	for page_num in range(10):
		page_url = get_url(page_num)
		html = get_html(page_url)
		items = get_info(html)
		write_info(items, page_num*25 + 1 ,test)
	for i in range(0,len(row0)):    
		test.write(0,i,row0[i],header_style) 
	f.save('movie250.xls')
	
if __name__=='__main__':
	f = xlwt3.Workbook()
	test = f.add_sheet(u'test', cell_overwrite_ok=True)
	save_file(f,test)
