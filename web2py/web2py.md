### web2py
   - Web2py is an open source web application framework written in the Python programming language. 
   - Web2py allows web developers to program dynamic web content using Python.

### install

````sh

   wget http://www.web2py.com/examples/static/web2py_src.zip
   
   unzip web2py_src.zip
   cd web2py

   # web2py is that you do not install it. You can run it right from this folder by typing
   python web2py.py


````

### 실행

````sh

   # firefox 에서
   http://127.0.0.1:8000

````

### hello world

````sh

   cd /usr/local/web2py/application/app1/controllers
   
   vim test.py
   
   def hello():
      return "hello"
   
   # http://127.0.0.1:8000/app1/test/hello
   
   def helloworld():
      return "<html><body><h1>Hello World</h1><body></html>"

   # http://127.0.0.1:8000/app1/test/helloworld

````

### 기상청 페이지 크롤링하여 온도값을 web2py 활용하여 웹페이지 표시

```sh

#!/usr/bin/python
# -*- coding: utf-8 -*- 

import urllib2 # extensible library for opening URLs
import time

from lxml.html import parse, fromstring # processing XML and HTML

# 인천 남구 용현동 기상상황 확인 url
url = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2823759100'
temp=[]

def temp_process():
        page = urllib2.urlopen(url).read()
        xml= fromstring(page)

        for  elt in xml.getiterator("temp"):    # getting temp tag 
                temp_val = elt.text

        return temp_val

```


### openTSDB 연동하여 웹페이지 표시

```sh

cd /usr/local/web2py/application/app1/views/default
vim index.html

```

```sh

<!DOCTYPE html>

<html>
        <head>
                <meta charset="utf-8" http-equiv="Refresh" content="600">
                <title> Test </title>
        </head>

        <body>
                <div class="container">
                        <div id="development-header" class="page-header">
                                <h1>Development</h1>
                        </div>

                        <div class="caption">
                                <h3>온도</h3>
                        </div>
                </div>

        </body>

</html>


```

### controller에서 value 넘기기

```sh

# cp /usr/local/app1/ /usr/local/app2 -rf
# cd /usr/local/app2/controllers
# vim defalut.py
# 기존 코드를 삭제 하고 아래 내용을 defalut.py 에 넣음
```


```sh

#!/usr/bin/python
# -*- coding: utf-8 -*- 

import urllib2 # extensible library for opening URLs
import time

from lxml.html import parse, fromstring # processing XML and HTML

# 인천 남구 용현동 기상상황 확인 url
url = 'http://www.kma.go.kr/wid/queryDFSRSS.jsp?zone=2823759100'
temp=[]

def index():
        page = urllib2.urlopen(url).read()
        xml= fromstring(page)

        for  elt in xml.getiterator("temp"):    # getting temp tag 
                temp_val = elt.text

        return locals()

```

```sh

# cd ..
# cd views/default
# vim index.html
# index.html 내 코드를 모드 삭제하고 아래 코드 입력

```

```sh

<!DOCTYPE html>
<html>
        <head>
                <meta charset="utf-8" http-equiv="Refresh" content="600">
                <title> Test </title>
        </head>

        <body>
                <div class="container">
                        <div id="development-header" class="page-header">
                                <h1>Development</h1>
                        </div>

                        <div class="caption">
                                <h3> temperature</h3>
                                <p>
                                {{=temp_val}}
                                </p>
                        </div>
                </div>

        </body>
</html>

```

```sh

# 웹브라우저
# http://127.0.0.1:8000/app2

```

### api 제작
#### 임의의 데이터를 openTSDB에 저장 

```sh

# 사전작업으로 temperature 데이터를 임의로 넣음
# matric : temperature
# tag : id = 1, 2
# value : 0, 10, 20, 30, 40, 50, 60 반복

```

```sh

#!/usr/bin/python
# -*- coding: utf-8 -*- 

import sys
import urllib2
import time
from datetime import datetime, timedelta
import json
import requests


url_local ="http://127.0.0.1:4242/api/put"

def insert(value, id):
        data={
                "metric":"temperature",
                "timestamp":time.time(),
                "value":value,
                "tags":{
                        "nodeid":id
                }
        }
        ret = requests.post(url_local, data=json.dumps(data))
        time.sleep(1)


if __name__ == '__main__':
        while 1 :
                t = time.localtime()
                tsec = t.tm_sec

                if tsec%10!=0:
                        print tsec
                        time.sleep(0.99)
                else :
                        try:
                                insert(tsec, 1)
                                insert(tsec+5, 2)
                                print tsec
                                time.sleep(0.99)
                        except:
                                print "error"
                                time.sleep(0.99)

```

#### max 값 구하기

```sh

# 사용할 어플리케이션 복사
# cp /usr/local/web2py/applications/app1 /usr/local/web2py/applications/max -rf
# cd /usr/local/web2py/applications/max/controllers
# vim test.py

# metric : temperature
# tag : id
# id : 1
```

```sh

# -*- coding: utf-8 -*-

import datetime
import urllib2
import json
import time

url = "http://127.0.0.1:4242/api/query?start=1m-ago&m=sum:temperature%7Bid=1%7D&o=&yrange=%5B0:%5D&key=out%20bottom%20center%20box&wxh=740x345&autoreload=15"

def make_data(raw_data):
        max_val = 0

        tmp_data = raw_data.replace('u' , '')
        tmp_data = raw_data.replace('{' , '')
        tmp_data = raw_data.replace("'" , '')
        tmp_data = raw_data.replace('}' , '')
        tmp_data = raw_data.split(',')

        for i in range(0, len(tmp_data)-1) :
                arr_data = tmp_data[i].split(':')
                arr_Time = arr_data[0].strip()
                arr_Value = arr_data[1].strip()

                if float(arr_Value) > float(max_val):
                        max_val = arr_Value
        return max_val

def test():
        max_value = 0
        max_time = 0
        param = request.vars['id']

        url_lib=urllib2.urlopen(url)
        url_data=url_lib.read()

        Data=json.loads(url_data)

        raw_data=str(Data[0]["dps"])
        result_max_val = make_data(raw_data)

        return result_max_val
        
```

```sh

# http://127.0.0.1:8000/max/test/test

```

#### max 값 구하는 api 만들기
##### id 에 따라 max값(최대값) 불러오는 api
###### http://127.0.0.1:8000/max/test?id=1
###### http://127.0.0.1:8000/max/test?id=2

```sh
# metric은 temperature
# tag는 id
# 아래 링크에 코딩
# vim /usr/local/web2py/applications/max/controls/test.py
```

```sh

# -*- coding: utf-8 -*-

import datetime
import urllib2
import json
import time

json_tmp = {}
rest_result = []

param_id = request.vars['id']

url = "http://127.0.0.1:4242/api/query?start=1m-ago&m=sum:temperature%7Bid=" + param_id + "%7D&o=&yrange=%5B0:%5D&key=out%20bottom%20center%20box&wxh=740x345&autoreload=15"

def make_json(max_val):
        json = {"max":{"id":param_id, "value":max_val}}
        return json

def make_data(raw_data):
        max_val = 0

        tmp_data = raw_data.replace('u' , '')
        tmp_data = raw_data.replace('{' , '')
        tmp_data = raw_data.replace("'" , '')
        tmp_data = raw_data.replace('}' , '')
        tmp_data = raw_data.split(',')

        for i in range(0, len(tmp_data)-1) :
                arr_data = tmp_data[i].split(':')
                arr_Time = arr_data[0].strip()
                arr_Value = arr_data[1].strip()

                if float(arr_Value) > float(max_val):
                        max_val = arr_Value
        return max_val

def test():
        param = request.vars['id']

        url_lib=urllib2.urlopen(url)
        url_data=url_lib.read()

        Data=json.loads(url_data)
        raw_data=str(Data[0]["dps"])

        # get max data using make_data function
        result_max_val = make_data(raw_data)

        json_tmp['1'] = make_json(result_max_val)

        rest_result.append(json_tmp['1'])
        ret = response.json(rest_result)
        return ret

```

#### min 값 구하는 api 만들기 연습
##### id 에 따라 min값(최소값) 불러오는 api
