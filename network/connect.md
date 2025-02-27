#### 아파트형 라즈베리 원격 접속

```
# 방제실 컴퓨터 접속 (보관함 서버 -> 설정 -> vpn목록 -> 아이피 확인)
ssh -p 2222 root@172.16.3.2
pw : tmshdnxmfl (스노우트리)

# 방제실 컴퓨터 접속 후 관리자 페이지 접속 가능
http://172.16.3.2/admin

# 비밀번호 틀리면 db에서 조회
id : admin
pw : 1111


# 라즈베리 ip 조회
ifconfig

# 공인 ip
enp0s20f0u1 : inet 118.32.29.247  netmask 255.255.255.128  broadcast 118.32.29.255

# 내부 네트워크 ip
enp2s0 : inet 10.0.205.11  netmask 255.255.0.0  broadcast 10.0.255.255

wlan : 와이파이 공유기 ip

```

#### 라즈베리 파이 접속 ip 찾기
```
# mysql 접속
mysql -u root -p or sudo mysql
pw : tmshdnxmfl (스노우트리)

# 데이터 베이스 선택
use yellobox;

# 라즈베리 파이 ip 찾기
select ip from applebox;

+-------------+
| ip          |
+-------------+
| 10.1.205.11 |
| 10.2.205.11 |
| 10.3.205.11 |
| 10.4.205.11 |
| 10.5.205.11 |
| 10.6.205.11 |
+-------------+


# 라즈베리파이 접속
ssh pi@10.1.205.11
pw : tmshdnxmfl (스노우트리)

# 라우팅 테이블 조회
route -n

ip route show


```

#### 라즈베리파이 하드웨어 정보
```
# 라즈베리파이의 모델(버전)을 확인
cat /proc/cpuinfo

Hardware: BCM2835
Revision: a020d3 → Raspberry Pi 3 Model B+


# System Information 항목 -> 모델확인 
sudo raspi-config


# 라즈비안 OS 버전을 확인
lsb_release -a

```

#### 운영체제(OS) 정보
```
OS: Raspbian GNU/Linux 9.13 (Stretch)
배포판: Raspbian (Debian 기반)
버전: 9.13 (Stretch, 2017년 출시)
```



