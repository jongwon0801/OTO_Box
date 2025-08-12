#### 회사 로컬 서버 접속
```less
ssh hizib@192.168.0.73

pw : wikibox
```

#### 수색 vpn 접속

```less
ssh -p 2222 root@10.0.0.3
pw : 스노우트리(tnsgdbxnfk)
```

#### DB 접속

```less
sudo mysql -u root -p
pw : 스노우트리

mysql -u yellowbox -p
pw : dpfshdnqkrtm (엘로우박스) (직접치지말고 복붙해야됨)
```


#### mysql 명령어
```less
# 유저 확인
SELECT User, Host FROM mysql.user; 

# yellowbox 권한 확인
SHOW GRANTS FOR 'yellowbox'@'%';

# 아이피 확인
select ip from applebox;

```

#### 라즈베리 ip
```less
+---------------+
| ip            |
+---------------+
| 10.101.80.101 |
| 10.101.80.102 |
| 10.102.80.101 |
| 10.102.80.102 |
| 10.103.80.101 |
| 10.103.80.102 |
| 10.104.80.101 |
| 10.104.80.102 |
| 10.105.80.101 |
| 10.105.80.102 |
| 10.106.80.101 |
| 10.106.80.102 |
| 10.107.80.101 |
| 10.107.80.102 |
| 10.108.80.101 |
| 10.108.80.102 |
+---------------+
```




#### 비즈뿌리오 경로
```less
/opt/biz_client_v3011

# 비즈 클라이언트 프로세스 실행 중 확인

ps -ef | grep "biz_client"
ps aux | grep biz

# 보관함에서 myslq 설치 확인
dpkg -l | grep -i mysql

# 보관함에서 서버접속
mysql -h 10.100.80.100 -P 3306 -u yellowbox -p
```




