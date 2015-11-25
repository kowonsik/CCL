#!/usr/bin/python

import sys
import urllib2
import json
import struct
import time
from datetime import datetime, timedelta

def dataParser(s):
    s = s.split("{")
    i = 0
    j = len(s)
    if j > 2:
        s = s[3].replace("}","")
        s = s.replace("]","")
    else:
        return '0:0,0:0'
    return s

while 1 :
    t = time.localtime()
    tsec = t.tm_sec
    if tsec%10!=0 :
    	print tsec
    	time.sleep(0.8)
        
    else :
        endTimeUnix = time.time()
        startTimeUnix = endTimeUnix - 1800 

        startTime = datetime.fromtimestamp(startTimeUnix).strftime('%Y/%m/%d-%H:%M:%S')
        endTime = datetime.fromtimestamp(endTimeUnix).strftime('%Y/%m/%d-%H:%M:%S')

        #print startTime
        #print endTime
	metric = 'cc_100.test'
        url = 'http://127.0.0.1:4242/api/query?start=' + startTime + '&end=' + endTime + '&m=sum:' + metric
        print url

        try:
            u = urllib2.urlopen(url)
        except:
	    raise NameError('url error')

        data = u.read()
	print data
        packets = dataParser(data)
        packet = packets.split(',')

        j=len(packet)

        v_s = packet[0].split(":")
        v_e = packet[j-1].split(":")

	print v_s[0], v_s[1]
        #print "cc.test %d %d" % ( endTimeUnix, v_e )
    	ime.sleep(0.8)
