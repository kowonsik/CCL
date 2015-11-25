github desktop

https://desktop.github.com/

----

## Ubuntu git 설치

```sh
sudo apt-get install git   
```

----

## CentOS git 설치
```sh
su

yum install git
```

----

## git 사용법
```sh
mkdir ~/workspace

cd ~/workspace

git status

git init

git status

git config --global user.name [유저이름]

git config --global user.email [이메일주소]

git remote add origin https://github.com/kowonsik/raspberry.git

git pull -u origin master     # 파일 다운로드

git add [생성한파일]

git status

git commit -m "메세지"

git status

git push -u origin master     # 파일 업데이트
```

-----
origin url 설정이 잘못되서 origin을 삭제(수정)해야할 경우

```sh
git remote rm origin

git remote rename origin origin_re
```

----

## git push error

### url return error

```sh
git remote set-url origin git@github.com:kowonsik/레포지터리이름.git
```

### public key error 참고링크

http://uiandwe.tistory.com/992

----
