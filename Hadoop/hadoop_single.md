```sh
    yum -y update
    yum install wget  # wget 설치가 되어있지 않은 경우에 실행
    systemctl stop firewalld  # 방화벽 해제가 필요한 경우에 실행
```

----
[ yum을 이용하여 Chrome 브라우저 설치 ] # 웹브라우저 설치가 필요한 경우에 실행

```sh

vi /etc/yum.repos.d/google.repo 

# 다음 내용 추가

[google64]
name=google-chrome - 64-bit
baseurl=http://dl.google.com/linux/rpm/stable/x86_64
enabled=1
gpgcheck=1
gpgkey=https://dl-ssl.google.com/linux/linux_signing_key.pub

```

```sh
# yum으로 Google Chrome 안정판 설치
yum install google-chrome-stable

#다음과 같은 에러가 발생하여 설치가 중단된다.

# Error: Package: google-chrome-stable-30.0.1599.114-1.x86_64 (google64)
#       Requires: libstdc++.so.6(GLIBCXX_3.4.15)(64bit)
#       
# Richard Lloyd가 만든 설치 스크립트를 이용하여 다시 설치

wget http://chrome.richardlloyd.org.uk/install_chrome.sh
chmod u+x install_chrome.sh
./install_chrome.sh

```
----

## Hadoop 설치하기

```sh

[기존 java 삭제하기] # centos 경우에는 자바 설치가 되어 있지 않으므로 따로 실행할 필요 없음

yum -y remove "java-*"

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

    vi /etc/profile

    밑에 export 3줄만 추가

    export JAVA_HOME=/usr/java/jdk1.8
    export PATH=$JAVA_HOME/bin:$PATH
    export CLASSPATH=$CLASSPATH:$JAVA_HOME/jre/lib/ext:$JAVA_HOME/lib/tools.jar

    # 실행
    source /etc/profile
```

    2. 계정 추가

```sh

    # SSH 설치 및 공개 키 설정 
    #   Hadoop클러스터에서 Master와 Slave들 간에 통신은 SSH를 이용함
    #   모든 컴퓨터에는  SSH가 설치되어 있어야 함
    #   Master에서 암호없이 Slave에 접속하기 위해서 공개 키가 필요함

    useradd hadoop
    su - hadoop
    ssh-keygen -t dsa -P '' -f ~/.ssh/id_dsa
    cat ~/.ssh/id_dsa.pub >> ~/.ssh/authorized_keys
    chmod 0600 ~/.ssh/authorized_keys
```

    3. 로컬호스트 들어갔다 나오기

```sh
    ssh localhost
    exit
```

    4. 하둡다운로드
    
```sh
    su
    cd /home
    mkdir hadoop
    cd hadoop
    wget http://apache.tt.co.kr/hadoop/common/hadoop-2.7.1/hadoop-2.7.1.tar.gz
    tar -zxvf hadoop-2.7.1.tar.gz
```

    5. 컨피규어링

```sh
    vi $HOME/.bashrc
    
    # 아래 11개 export 만 추가해주면 됨
    export JAVA_HOME=/usr/java/jdk1.8
    export HADOOP_CLASSPATH=${JAVA_HOME}/lib/tools.jar
    export HADOOP_HOME=/home/hadoop/hadoop-2.7.1
    export HADOOP_INSTALL=$HADOOP_HOME
    export HADOOP_MAPRED_HOME=$HADOOP_HOME
    export HADOOP_COMMON_HOME=$HADOOP_HOME
    export HADOOP_HDFS_HOME=$HADOOP_HOME
    export HADOOP_YARN_HOME=$HADOOP_HOME
    export HADOOP_COMMON_LIB_NATIVE_DIR=$HADOOP_HOME/lib/native
    export PATH=$PATH:$HADOOP_HOME/sbin:$HADOOP_HOME/bin
    export JAVA_LIBRARY_PATH=$HADOOP_HOME/lib/native:$JAVA_LIBRARY_PATH

    # 실행
    source $HOME/.bashrc
```

    6. 설정값 추가하기

![connection](https://github.com/kowonsik/CCL/blob/master/lecture/hadoop.png)
![connection](https://github.com/kowonsik/CCL/blob/master/lecture/name_data_node.png)


```sh
    # (하둡을 구동하는 스크립트에서 사용되는 환경 변수)
    vi $HADOOP_HOME/etc/hadoop/hadoop-env.sh 
    export JAVA_HOME=/usr/java/jdk1.8
```

------------------------------------------

```sh
    # Hadoop 설치 후 로그파일, 네트워크 튜닝, I/O튜닝, 파일 시스템 튜닝, 압축 등과 같이 기본적인 하부 시스템 설정
    # 맵리듀스에서도 공통으로 사용
    
    vi $HADOOP_HOME/etc/hadoop/core-site.xml
    
    <configuration> 
        <property>
            <name>fs.default.name</name>
            <value>hdfs://localhost:9000</value>
        </property>
    </configuration> 
```

-------------------------------------------------

```sh
    # (네임노드, 보조 네임노드, 데이터노드 등과 같은 HDFS 데몬을 위한 환경 설정 구성)
    vi $HADOOP_HOME/etc/hadoop/hdfs-site.xml
    
    <configuration> 
        <property>
            <name>dfs.replication</name>
            <value>1</value>
        </property>
 
        <property>
            <name>dfs.name.dir</name>
            <value>file:///home/hadoop/hadoopdata/hdfs/namenode</value>
        </property>
 
        <property>
            <name>dfs.data.dir</name>
            <value>file:///home/hadoop/hadoopdata/hdfs/datanode</value>
        </property>
    </configuration>         
```

-------------------------------------------------

```sh
    # 실행
    cp $HADOOP_HOME/etc/hadoop/mapred-site.xml.template $HADOOP_HOME/etc/hadoop/mapred-site.xml
    
```
-------------------------------------------------

```sh
    # (잡트래커와 테스크트래커와 같은 맵리듀스 데몬을 위한 환경 설정 구성)
    vi  $HADOOP_HOME/etc/hadoop/mapred-site.xml
    
    <configuration> 
        <property>
            <name>mapreduce.framework.name</name>
            <value>yarn</value>
        </property>
    </configuration> 
```

-------------------------------------------------

```sh
    vi $HADOOP_HOME/etc/hadoop/yarn-site.xml

    <property>
        <name>yarn.nodemanager.aux-services</name>
        <value>mapreduce_shuffle</value>
    </property>
```

-------------------------------------------------

```sh
    # 실행
    set JAVA_HOME
```


    7. 하둡시작
    
```sh
    hdfs namenode -format
    start-dfs.sh
    start-yarn.sh
```
    8. Web GUI 확인

```sh    
    # 웹브라우저(firefox)를 열고 테스트
    localhost:50070  # NameNode 정보 확인
    localhost:50090  # Secondary NameNode 정보 확인
    localhost:8088   # 클러스터와 모든 어플리케이션 정보 확인
```
    9. word counting example

```sh
    # 테스트 문서 제작
    vim test.txt
    
    # 아래 두줄을 test.txt 에 넣어주면 됨
    # 테스트용 문서를 옮겨놓고 사용해도 됨)
    i am a boy
    you are a girl
    
    hdfs dfs -mkdir /user   # user 디렉토리를 만듬 # exist directory 인 경우는 패스하면 됨
    hdfs dfs -mkdir /user/hadoop   # hadoop 디렉토리를 만듬 # exist directory 인 경우는 패스하면 됨
    hdfs dfs -mkdir /user/hadoop/input   # input 디렉토리를 만듬
    hdfs dfs -put test.txt /user/hadoop/input   # test.txt 파일을 input 디렉토리에 넣음
    
    # Word Count java 코드 작성( github 에서 WordCount.java 파일 다운로드)
    wget https://raw.githubusercontent.com/kowonsik/CCL/master/WordCount.java
    
    # WordCount.java compile
    hadoop com.sun.tools.javac.Main WordCount.java
    
    # jar 파일 만들기
    jar -cf wc.jar WordCount*.class
    
    # Word Count 실행
    hadoop jar wc.jar WordCount /user/hadoop/input /output
    
    # 결과 확인
    hdfs dfs -cat /output/part-r-00000
    
    # 기본 파일 명령어
    hadoop fs -ls /   # 모든 디렉토리 확인
    hadoop fs -ls /output   # output 디렉토리 확인 
    hadoop fs -rmr /output   # output 디렉토리 삭제
    
```
