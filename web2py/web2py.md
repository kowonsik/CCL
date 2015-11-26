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
                                <h3>미세먼지 수치</h3>
                        </div>
                </div>

        </body>

</html>


```
