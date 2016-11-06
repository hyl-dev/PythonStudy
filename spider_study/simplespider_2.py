#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import urllib.request
import urllib.parse
import re
import redis
import time

MAX_LIMIT = 10

class Database(object):
  def __init__(self, ip, port):
    self.ip = ip
    self.port = port
    self.write_pool = {}

  def add_data(self, movie_tag, title, ratingnum):
    key = '_'.join([movie_tag, title]);
    value = ratingnum
    self.write_pool[key] = value

  def batch_write(self):
    try:
      client = redis.StrictRedis( host =self.ip, port=self.port)
      client.mset(self.write_pool)
	  keys = client.keys()
	  print(keys)
    except Exception as exception:
      print(exception)


def movie_spider(db, url, count=1):
  if count > MAX_LIMIT:
    return
  count += 1
  html = urllib.request.urlopen(url)
  data = html.read().decode('utf8', 'ignore')
  data = data.replace('\n', '')
  lists = re.findall(r'<tr class="item">(.*)</tr>', data)
  if len(lists) == 0:
    return
  lists = lists[0].split('</tr>')
  for movie_info in lists:
    title = re.findall(r'title=([^>]+)>', movie_info)
    mark_num = re.findall(r'<span class="rating_nums">(\d.\d)</span>', movie_info)
    #totalcount=re.findall(r'<span class="pl">((\d)人评价)</span>',movie_info)
    if len(mark_num) == 0 or len(title) == 0:
      continue
    if float(mark_num[0]) > 8.0:
      db.add_data(movie_info,title[0],mark_num[0])
    else:
      continue
  nextrurl = str(re.findall(r'<link rel="next" href="([^>]*)"/>', data)[0])
  if 'http' in nextrurl:
    time.sleep(5)
    movie_spider(db, nextrurl, count)
  else:
    return

def spider_2(db):
  url = 'http://movie.douban.com/tag/'
  movie_list = ['喜剧', '科幻', '动作', '犯罪', '情色', '剧情', '搞笑', '悬疑', '魔幻', '音乐']
  for tag in movie_list:
    new_url = url + urllib.parse.quote(tag)
    movie_spider(db, new_url, count=1)

if __name__ == '__main__':
  db = Database('192.168.108.136', 6379)
  spider_2(db)
  db.batch_write()
 

