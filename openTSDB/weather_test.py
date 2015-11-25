#!/usr/bin/python
# -*- coding: utf-8 -*- 

##################################################
# 기상청
# http://www.kma.go.kr/weather/lifenindustry/sevice_rss.jsp

# RSS : 웹사이트 상의 컨텐츠를 요약하고 상호 공유할 수 있도록 만든 표준 XML을 기초로 만들어진 데이터 형식
# RSS 인천 용현동1,4
# http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2817055500

# install lxml library
# pip install python-lxml
##################################################

import urllib2 # extensible library for opening URLs
import time

from lxml.html import parse, fromstring # processing XML and HTML

# 인천 남구 용현동 기상상황 확인 url
url = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2823759100'
temp=[]

def temp_process(xml):
	for  elt in xml.getiterator("temp"):	# getting temp tag 
		temp_val = elt.text
		print temp_val

def time_print():
	now_unix = time.time()	# unix time
	now = time.localtime()	# local time

	now_year = now.tm_year	# year
	now_mon = now.tm_mon	# month
	now_day = now.tm_mday	# day
	now_hour = now.tm_hour	# hour 
	now_min = now.tm_min	# min
	now_sec = now.tm_sec	# sec

	print "======================="
	print now_unix	# unix time print
	print now
	print "======================="
	print now_year, now_mon, now_day, now_hour, now_min, now_sec	# time parsing
	print "======================="

if __name__ == '__main__':

	# time print function
	time_print()

	page = urllib2.urlopen(url).read()

	# fromstring : Parses an XML document or fragment from a string. 
	# Returns the root node (or the result returned by a parser target).
	xml_raw = fromstring(page)

	# processing temperature
	temp_process(xml_raw)

