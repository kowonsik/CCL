
## Hadoop
   - 전체 또는 부분 데이터에 대해 다양한 분석 수행
   - 대용량 처리를 위해 분산, 병렬 처리 필요

## HBase(http://hbase.apache.org/)
   - 원본 데이터를 실시간으로 저장, 조회, 처리를 위한 저장소
   - Hadoop의 서브프로젝트로 시작하여 지금은 Apache 정식 프로젝트가 되었으며, HBase란 이름은 Hadoop database에서 유래됨
   - Hadoop의 “분산된,확장가능한,대용량 데이터를 다루는” 특징을 물려받으면서 ” Random, realtime read/write access”라는 고유한 데이터베이스스러운 특징도 가지고 있음.
   - 관계형 데이터베이스가 아닌 NoSQL 데이터베이스로 분류되고, 기존 SQL문을 일부만 지원하며, column-oriented 로 데이터를 저장.
   
## openTSDB(http://opentsdb.net)
  - HBase와 연계하여 시계열 데이터를 관리
  - OpenTSDB is a tool that includes a time series database (built on hBase) and a web UI that uses GNUPlot for charting.
   
![opentsdb](https://raw.githubusercontent.com/kowonsik/CCL/master/openTSDB/png/opentsdb.png)

## OpenTSDB Install

### centos update
```sh
# root 권한으로 필요시 수행
   yum -y update

```

-----
### JAVA Setting
```sh

[기존 java 삭제하기] 
# 기존 시간에 설정한 사람은 다시 할 필요 없음
# yum -y remove "java-*"

```

    1. jdk 다운로드
```
arch명령어를 통해 비트수 확인 후 설치
```


```sh
    cd ~/Downloads

    (64비트인 경우)
    wget —no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u5-b13/jdk-8u5-linux-x64.tar.gz

    (32비트인 경우)
    wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/8u60-b27/jdk-8u60-linux-i586.tar.gz"
    

    cd ~/Downloads/
    tar –zxvf jdk-8u5-linux-x64.tar.gz
    mkdir /usr/java
    mv jdk1.8.0_05 /usr/java/jdk1.8

    vim /etc/profile

    밑에 export 3줄만 추가

    export JAVA_HOME=/usr/java/jdk1.8
    export PATH=$JAVA_HOME/bin:$PATH
    export CLASSPATH=$CLASSPATH:$JAVA_HOME/jre/lib/ext:$JAVA_HOME/lib/tools.jar

    # 실행
    source /etc/profile
```

-----

### hbase Install(버전이 바뀔수도 있음)
```sh
    cd /usr/local
    mkdir data
    cd data
    wget http://www.apache.org/dist/hbase/stable/hbase-1.1.2-bin.tar.gz
    tar xvfz hbase-1.1.2-bin.tar.gz
    cd hbase-1.1.2
    hbase_rootdir=${TMPDIR-'/usr/local/data'}/tsdhbase
    iface=lo'uname | sed -n s/Darwin/0/p'
```
##### hbase-site.xml correction
```sh
    vim conf/hbase-site.xml
```
configuration Add to between the tags
```sh
<configuration>
	<property>
		<name>hbase.rootdir</name>
		<value>file:///DIRECTORY/hbase</value>
	</property>
	<property>
		<name>hbase.zookp.property.eataDir</name>
		<value>/DRECTORY/zookeeper</value>
	</property>
</configuration>
```
##### hbase.sh Run
```sh
    ./bin/start-hbase.sh
    # master running as process (process number). Stop it first
```
※When " hbase.sh " run, If this is notification because the setting of the 'java_home JDK' is not successful,
  Run a " profile " again ($ source /etc/profile)

### GnuPlot Install
```sh
    cd /usr/local
    yum install ant ant-nodeps lzo-devel.x86_64
    yum list \*gd\*
    yum install gd-devel.i686
    wget http://sourceforge.net/projects/gnuplot/files/gnuplot/4.6.3/gnuplot-4.6.3.tar.gz
    tar zxvf gnuplot-4.6.3.tar.gz
    cd gnuplot-4.6.3
    ./configure
    make install
    yum install gnuplot
    # apt-get install dh-autoreconf
```
### OpenTSDB Install
  ```sh
    cd /usr/local
    
    # 필요시 yum install git
    git clone git://github.com/OpenTSDB/opentsdb.git

    cd opentsdb
    yum install autoconf
    yum install automake
    ./build.sh  <- It takes about 10 minutes to complete.
    env COMPRESSION=NONE HBASE_HOME=/usr/local/data/hbase-1.1.2 ./src/create_table.sh 
    tsdtmp=${TMPDIR-'/usr/local/data'}/tsd
    mkdir -p "$tsdtmp"
```
### Open TSDB Run
```sh
    ./build/tsdb tsd --port=4242 --staticroot=build/staticroot --cachedir=/usr/local/data --auto-metric

    # 웹브라우저에서 확인
    http://127.0.0.1:4242

```
![association](https://raw.githubusercontent.com/kowonsik/CCL/master/lecture/localhost.png)

### Data Input Test(Restful 방법)

```sh
# openTSDB 동작중인 터미널은 닫지 말고..
# 새로운 터미널을 열고 진행하세요...

sudo yum install python-setuptools python-setuptools-devel
sudo easy_install pip
pip install requests

vim post_test.py
```

```sh
import time
import requests
import json

url = "http://127.0.0.1:4242/api/put"

data = {
    "metric": "foo.bar",
    "timestamp": time.time(),
    "value": 2015,
    "tags": {
       "host": "mypc"
    }
}

ret = requests.post(url, data=json.dumps(data))
print "ok"
```

```sh

python post_test.py

    # 웹브라우저에서 확인
    http://127.0.0.1:4242

```

![association](https://raw.githubusercontent.com/kowonsik/CCL/master/openTSDB/png/opentsdb_insert_test.png)


```sh

# 웹브라우저에서 확인
http://127.0.0.1:4242/api/query?start=2015/10/14-00:00:00&end=2015/10/14-08:19:49&m=sum:foo.bar

# 결과
[{"metric":"foo.bar","tags":{"host":"mypc"},"aggregateTags":[],"dps":{"1444835983":2015.0}}]
```

### Temperature Input Test(Restful 방법)
   - 위에 데이터 입력 코드와 아래 기상청에서 온도 가져오는 코드를 활용하여 openTSDB에 데이터를 입력하세요
```sh

yum install python-lxml

vim weather_test.py

#!/usr/bin/python
# -*- coding: utf-8 -*- 

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

```
```sh

	python weather_test.py
```

### Tcollector Install
Execution of one terminal anymore
```sh
    cd /usr/local
    git clone git://github.com/OpenTSDB/tcollector.git
    cd tcollector
```
##### 'startstop' Changing the file
```sh
    vim startstop
```
Please comment cancel the portion of the '#TSD_HOST=dns.name.of.tsd' and Enter the Ip address.(4~5 line)
```sh
    TSD_HOST=192.168.X.X
```
### Tcollector Run - Execution of one terminal anymore
```sh
    ./startstop start

```
##### The connection with 'http://192.168.x.x:4242' in the web address bar


### tcollector Test

```sh
   # root 권한으로
   cd /usr/local/tcollector/collectors/0
   
```

#### test code 만들기 

```sh
   vim insert_test.py
```

```sh

#!/usr/bin/python

import sys
import urllib2
import time
from datetime import datetime, timedelta

while 1 :
    t = time.localtime()
    tsec = t.tm_sec
    if tsec%10!=0 :
            print tsec
            time.sleep(0.2)

    else :
        print "inha.test %d %d" % ( time.time(), tsec )
        time.sleep(0.1)

```

```sh
   # 실행해 보기
   python insert_test.py
   
   # 파일 권한 변경(참고 블로그 : http://blog.naver.com/radii26omg/220337573729)
   chmod 777 insert_test.py
   
   # openTSDB GUI에서 확인
   # http://127.0.0.1:4242
   
   # log 파일 확인
   # 터미널에서 실행
   tail -f /var/log/tcollector.log
   
   # 터미닐에서 실행 - 특정 단어만 검색
   tail -f /var/log/tcollector.log | grep inha
```

#### 연습 1

```sh
   # 20초마다 100을 openTSDB에 저장하세요
   # 메트릭 이름 변경(원하는 메트릭을 정하세요(예: cc_100))
```

#### 연습 2 : Tag 추가하기

```sh
   # 20초마다 100을 openTSDB에 저장하세요
   # 원하는 메트릭을 정하세요(예: cc_100)
   
   # insert_test.py 의 print 부분에 tag 를(id) 추가하세요(Tag는 7개까지 추가 가능)
   
   print "inha.test %d %d id = %d" % ( time.time(), tsec, 1030 )
   
```
