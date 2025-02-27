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

# 현황 버튼을 눌러서 ip 조회가능 링크에 표시됨
```

#### ip 조회
```
# 라즈베리 ip 조회
ifconfig

# 공인 ip
enp0s20f0u1 : inet 118.32.29.247  netmask 255.255.255.128  broadcast 118.32.29.255

# 내부 네트워크 ip
enp2s0 : inet 10.0.205.11  netmask 255.255.0.0  broadcast 10.0.255.255

wlan : 와이파이 공유기 ip
```

```
route -n

Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         118.32.29.254   0.0.0.0         UG    100    0        0 enp0s20f0u1
10.0.0.0        0.0.0.0         255.255.0.0     U     101    0        0 enp2s0
10.0.0.0        10.0.0.254      255.0.0.0       UG    101    0        0 enp2s0
118.32.29.128   0.0.0.0         255.255.255.128 U     100    0        0 enp0s20f0u1
172.16.0.0      0.0.0.0         255.255.0.0     U     0      0        0 vpn_soft
172.25.1.0      0.0.0.0         255.255.255.0   U     0      0        0 tap_soft

ip route show

default via 118.32.29.254 dev enp0s20f0u1 proto dhcp metric 100 
10.0.0.0/16 dev enp2s0 proto kernel scope link src 10.0.205.11 metric 101 
10.0.0.0/8 via 10.0.0.254 dev enp2s0 proto static metric 101 
118.32.29.128/25 dev enp0s20f0u1 proto kernel scope link src 118.32.29.247 metric 100 
172.16.0.0/16 dev vpn_soft proto kernel scope link src 172.16.3.2 
172.25.1.0/24 dev tap_soft proto kernel scope link src 172.25.1.1 

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
```

# 라즈베리파이 접속
```
# 라즈베리파이 접속
ssh pi@10.1.205.11
pw : tmshdnxmfl (스노우트리)

# 라우팅 테이블 조회
route -n

Kernel IP routing table
Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
0.0.0.0         10.1.0.254      0.0.0.0         UG    202    0        0 eth0
10.1.0.0        0.0.0.0         255.255.0.0     U     202    0        0 eth0
172.24.1.0      0.0.0.0         255.255.255.0   U     304    0        0 wlan0


ip route show

default via 10.1.0.254 dev eth0 src 10.1.205.11 metric 202 
10.1.0.0/16 dev eth0 proto kernel scope link src 10.1.205.11 metric 202 
172.24.1.0/24 dev wlan0 proto kernel scope link src 172.24.1.1 metric 304 

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



