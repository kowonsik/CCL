#### exercise 1
   - 주기적으로 증가하는 데이터를 openTSDB에 저장

```sh
vim test.py
```

```sh

#!/usr/bin/python

import sys
import urllib2
import time
from datetime import datetime, timedelta
import json
import requests

url ="http://127.0.0.1:4242/api/put"

def insert(value):
        data={
                "metric":"foo.bar",
                "timestamp":time.time(),
                "value":value,
                "tags":{
                        "host":"mypc"
                }
        }
        ret = requests.post(url, data=json.dumps(data))
        print ret
        time.sleep(1)

if __name__ == '__main__':

	while 1 :
        	t = time.localtime()
        	tsec = t.tm_sec

        	if tsec%10!=0 :
                	print tsec
                	time.sleep(1)
        	else :
                	insert(1111)	
```

```sh

성공
200 - 클라이언트의 요청을 정상적으로 수행하였을때 사용합니다. 응답 바디(body)엔 요청과 관련된 내용을 넣어줍니다. 그리고 200의 응답 바디에 오류 내용을 전송하는데 사용해서는 안된다고 합니다. 오류가 났을땐 40x 응답 코드를 권장합니다.
201 - 클라이언트가 어떤 리소스 생성을 요청하였고, 해당 리소스가 성공적으로 생성되었을때 사용합니다.
202 - 클라이언트의 요청이 비동기적으로 처리될때 사용합니다. 응답 바디에 처리되기까지의 시간 등의 정보를 넣어주면 좋다고 합니다.
204 - 클라이언트의 요청응 정상적으로 수행하였을때 사용합니다. 200과 다른점은 204는 응답 바디가 없을때 사용합니다. 예를들어 DELETE와 같은 요청시에 사용합니다. 클라이언트의 리소스 삭제요청이 성공했지만 부가적으로 응답 바디에 넣어서 알려줄만한 정보가 하나도 없을땐 204를 사용합니다.

실패
400 - 클라이언트의 요청이 부적절할때 사용합니다. 요청 실패시 가장 많이 사용될 상태코드로 예를들어 클라이언트에서 보낸 것들이 서버에서 유효성 검증(validation)을 통과하지 못하였을때 400으로 응답합니다. 응답 바디에 요청이 실패한 이유를 넣어줘야 합니다.
401 - 클라이언트가 인증되지 않은 상태에서 보호된 리소스를 요청했을때 사용하는 요청입니다. 예를들어 로그인(login)하지 않은 사용자가 로그인했을때에만 요청 가능한 리소스를 요청했을때 401을 응답합니다.
403 - 사용자 인증상태와 관계 없이 응답하고싶지 않은 리소스를 클라이언트가 요청했을때 사용합니다. 그러나 해당 응답코드 대신 400을 사용할 것을 권고합니다. 그 이유는 일단 403 응답이 왔다는것 자체는 해당 리소스가 존재한다는 뜻입니다. 응답하고싶지 않은 리소스는 존재 여부 조차 감추는게 보안상 좋기때문에 403을 응답해야할 요청에 대해선 그냥 400이나 404를 응답하는게 좋겠습니다.
404 - 클라이언트가 요청한 리소스가 존재 하지 않을때 사용하는 응답입니다.
405 - 클라이언트가 요청한 리소스에서는 사용 불가능한 Method를 이용했을때 사용하는 응답입니다. 예를들어 읽기전용 리소스에 DELETE Method를 사용했을때 405 응답을 하면 됩니다.

기타
301 - 클라이언트가 요청한 리소스에 대한 URI가 변경 되었을때 사용합니다. 응답시 Location header에 변경된 URI를 적어줘야 합니다.
500 - 서버에 뭔가 문제가 있을때 사용합니다.

```

   
#### exercise 2
   - 주기적으로 특정 웹페이지(http://www.airkorea.or.kr) 크롤링하여 openTSDB에 저장 (미세먼지)
   - ex1 번의 json 데이터를 추가하여 작성..metric은 변경하여 사용하길 바라(참고:dust)
   - url 중복 확인, split 한 변수가 string이므로 int로 형변환 int(c[1])

##### 참고
```sh

#!/usr/bin/python
# -*- coding: utf-8 -*- 

import urllib2 # extensible library for opening URLs
import time

# 인천 미세먼지 
url = 'http://www.airkorea.or.kr/index'


def getData(buffers):
	a = buffers.split('<tbody id="mt_mmc2_10007">')[1]
	#print a
	
	b = a.split('</tbody>')[0].replace('<tr>','').replace('</tr>','').replace('</td>','')
	#print b

	c = b.split('<td>')
	#print c[1]
	#print c[2]

if __name__ == '__main__':

	page = urllib2.urlopen(url).read()
	print page

	getData(page)

```

##### 아래 코드를 참고하여 서울과 인천의 미세먼지 수치를 openTSDB에 저장하고 웹에서 확인

```sh

#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys
import urllib2
import time
from datetime import datetime, timedelta
import json
import requests


# 인천 미세먼지 
url = 'http://www.airkorea.or.kr/index'
url_local ="http://127.0.0.1:4242/api/put"

def insert(metric_name, tag_site, value):
	data={
		"metric":metric_name,
		"timestamp":time.time(),
		"value":value,
		"tags":{
			"site":tag_site
		}
	}
	ret = requests.post(url_local, data=json.dumps(data))
	time.sleep(1)


def getData(buffers):
	a = buffers.split('<tbody id="mt_mmc2_10007">')[1]
	#print a
	
	b = a.split('</tbody>')[0].replace('<tr>','').replace('</tr>','').replace('</td>','')
	#print b

	c = b.split('<td>')
	# seoul
	print c[1]
	print c[2]

	# incheon
	print c[7]
	print c[8]

	insert('dust', 'incheon', int(c[8]))
	time.sleep(1)

if __name__ == '__main__':
	while 1 :
		t = time.localtime()
		tsec = t.tm_sec
		
		if tsec%10!=0:
			print tsec
			time.sleep(1)
		else :
			page = urllib2.urlopen(url).read()
			getData(page)

```
   
   
#### exercise 3
   - 기상청 웹페이지(http://www.kma.go.kr/weather/lifenindustry/sevice_rss.jsp) 
   - xml 형태로 리턴해줌
   - 크롤링하여 온도를 출력하고 openTSDB에 저장

##### 참고
```sh

#!/usr/bin/python
# -*- coding: utf-8 -*- 

##################################################
# 기상청
# http://www.kma.go.kr/weather/lifenindustry/sevice_rss.jsp

# RSS : 웹사이트 상의 컨텐츠를 요약하고 상호 공유할 수 있도록 만든 표준 XML을 기초로 만들어진 데이터 형식
# RSS 인천 용현동1,4
# http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2817055500

# lxml library 설치해야함
# yum install python-lxml
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

if __name__ == '__main__':
	page = urllib2.urlopen(url).read()
	print page
	
	# fromstring : Parses an XML document or fragment from a string. 
	# Returns the root node (or the result returned by a parser target).
	xml_raw = fromstring(page)

	# processing temperature
	temp_process(xml_raw)

```

#### exercise 4
   - openTSDB API 호출하고 json 형식의 데이터를 파싱
   - 호출 url
```sh
http://125.7.128.53:4242/#start=10m-ago&m=sum:gyu_RC1_thl.temperature%7Bnodeid=2454%7D&o=&key=out%20bottom%20center%20box&wxh=600x300&autoreload=15
```

   - json 형식의 데이터 호출
```sh
http://125.7.128.53:4242/api/query?start=10m-ago&m=sum:gyu_RC1_thl.temperature%7Bnodeid=2454%7D&o=&key=out%20bottom%20center%20box&wxh=600x300&autoreload=15
```


```sh

#!/usr/bin/python

import sys
import urllib2
import json
import struct
import time
from datetime import datetime, timedelta

url = 'http://125.7.128.53:4242/api/query?start=10m-ago&m=sum:gyu_RC1_thl.temperature%7Bnodeid=2454%7D&o=&key=out%20bottom%20center%20box&wxh=600x300&autoreload=15'

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

if __name__ == '__main__':

	while 1 :
		t = time.localtime()
		tsec = t.tm_sec
		
		if tsec%10!=0 :
			print tsec
			time.sleep(0.8)
		else :
			#endTimeUnix = time.time()
			#startTimeUnix = endTimeUnix - 1800 
			#startTime = datetime.fromtimestamp(startTimeUnix).strftime('%Y/%m/%d-%H:%M:%S')
			#endTime = datetime.fromtimestamp(endTimeUnix).strftime('%Y/%m/%d-%H:%M:%S')
			#print startTime
			#print endTime
			#metric = 'cc_100.test'
			#url = 'http://127.0.0.1:4242/api/query?start=' + startTime + '&end=' + endTime + '&m=sum:' + metric
			#print url
			
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
			time.sleep(0.8)

```

#### exercise 5
- exercise 5번에서 자신의 openTSDB 데이터(127.0.0.1)를 이용하여 실행하세요
- 인천지역 온도값을 출력


#### exercise 6
- serial 로 데이터를 수신하고 openTSDB에 저장

- 윈도우에서 USB 드라이버 설치 : http://125.7.128.52:8001/wordpress/pub/inhatc/CDM_Setup.exe
- serial 사용을 위한 python 라이브러리 설치
```sh

# pyserial install
wget http://sourceforge.net/projects/pyserial/files/pyserial/2.7/pyserial-2.7.tar.gz
tar xvfz pyserial-2.7.tar.gz
cd pyserial-2.7
python setup.py install

vim serial_to_openTSDB.py
```

```sh

#!/usr/bin/python

import time
import os
import sys
import serial

packet =''

def bigEndian(s):
        res = 0
        while len(s):
                s2 = s[0:2]
                s = s[2:]
                res <<=8
                res += eval('0x' + s2)
        return res

def sese(s):

        head = s[:20]
        type = s[36:40]

        serialID = s[24:36]
        nodeID = s[55:56]
        seq = s[40:44]

        batt = s[60:64]


        if type == "0070" : # TH
                #print s
                print "battery : " , bigEndian(batt)
                temperature = bigEndian( s[64:68] )
                v1 = -39.6 + 0.01 * temperature

                t = int(time.time())
                print "temperature %d %.2f nodeid=%d" % ( t, v1, bigEndian( nodeID ) )

        else:
                #print >> sys.stderr, "Invalid type : " + type
                pass

if __name__ == '__main__':

        tmpPkt = []
        flag = 0

        test = serial.Serial("/dev/ttyUSB0", 115200)

        while 1:
                Data_in = test.read().encode('hex')

                if(Data_in == '7e'):
                        if(flag == 2) :
                                flag =0
                                tmpPkt.append(Data_in)
                                packet = ''.join(tmpPkt)

                                # send packet
                                sese(packet)

                                tmpPkt = []
                                sys.stdout.flush()
                        else :
                                flag = flag + 1
                                tmpPkt.append(Data_in)
                else :
                        if(flag == 1 and Data_in =='45') :
                                flag =2
                        tmpPkt.append(Data_in)


```
