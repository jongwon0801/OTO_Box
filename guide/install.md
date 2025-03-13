#### 보관함 생성 (기존 등록된 데이터 그대로 사용)

```
공통코드 확인 swagger
http://smart.apple-box.kr/api/#!/%EA%B3%B5%ED%86%B5%EC%BD%94%EB%93%9C/codeTblList

gCode : locker.status 
```

#### 1. 관리자 페이지

1-1 서버 관리자 페이지

smart.apple-box.kr/buyer 네이버 보관함 서버에 buyer 계정을 생성해서 하는 방법

관리자 ID PW 생성

1-2 라즈베리 자체 관리자 페이지
```
# 춘의동 세탁소는 관리자페이지 없음 예시용
http://192.168.0.20/admin
```
방제실에 pc에서 라즈베리파이에서 실행중인 데몬의 관리자 페이지에 들어가는 방법



#### 2. 보관함 현황

2-1 네이버 서버의 보관함 -> 설치목록 -> 락커현황

서버 DB에 등록된 락커 설정파일을 불러온다

2-2 오투오박스보기

실제 라즈베리파이와 통신해서 현재 현황을 가져온다



#### 3. 설치파일

3-1 "yid" : 20051 값으로 이미 저장된 설정으로 새로 생성가능

3-2

```
sudo install.sh 11096 wifi

# 코드번호로 라즈베리파이에 접속한 상태로 설치를 진행
(필요하면 컨트롤러 불필요한 부분 삭제가능)

python export.py 11088
python export.py -t locker

# 필요한 log 조회 가능
cd newapp

cd logs

vi django.log

sudo find . -name "*.log" | xargs grep 01041640527
```








