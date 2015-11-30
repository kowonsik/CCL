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
