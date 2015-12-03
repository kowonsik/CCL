
### api 제작
   - 임의의 데이터를 openTSDB에 저장 

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

   - max 값 구하기

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

   - http://127.0.0.1:8000/max/test/test

### API 만들기


   - id 에 따라 max값 불러오는 api
   - http://127.0.0.1:8000/max/test?id=1
   - http://127.0.0.1:8000/max/test?id=2

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

#### [연습] min 값 구하는 api 만들기
   - id 에 따라 min값 불러오는 api
