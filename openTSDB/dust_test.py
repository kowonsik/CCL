#!/usr/bin/python
# -*- coding: utf-8 -*- 

import urllib2 # extensible library for opening URLs
import time
import sys
import urllib2
from datetime import datetime, timedelta
import json
import requests

# 인천 미세먼지 
url = 'http://www.airkorea.or.kr/index'
url_local ="http://127.0.0.1:4242/api/put"


def insert(value):
        data={
                "metric":"dust",
                "timestamp":time.time(),
                "value":value,
                "tags":{
                        "host":"mypc"
                }
        }
        ret = requests.post(url_local, data=json.dumps(data))
        print ret


def getData(buffers):
	a = buffers.split('<tbody id="mt_mmc2_10007">')[1]
	#print a
	
	b = a.split('</tbody>')[0].replace('<tr>','').replace('</tr>','').replace('</td>','')
	#print b

	c = b.split('<td>')
	print c[1]
	print c[2]
	
	insert(int(c[8]))

if __name__ == '__main__':

	page = urllib2.urlopen(url).read()
	#print page

	getData(page)

