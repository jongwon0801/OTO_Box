#### 아파트형 라즈베리 원격 접속

```
# 방제실 컴퓨터 접속 (보관함 서버 -> 설정 -> vpn목록 -> 아이피 확인)
ssh -p 2222 root@172.16.3.2
pw : tmshdnxmfl (스노우트리)

# 라즈베리 ip 조회
ifconfig

# 공인 ip
enp0s20f0u1 : inet 118.32.29.247  netmask 255.255.255.128  broadcast 118.32.29.255

# 라즈베리 ip
enp2s0 : inet 10.0.205.11  netmask 255.255.0.0  broadcast 10.0.255.255

wlan : 와이파이 공유기 ip

```

#### 라즈베리파이 하드웨어 정보
```
Hardware: BCM2835
Revision: a020d3 → Raspberry Pi 3 Model B+
운영체제(OS) 정보
```

#### os 정보
```
OS: Raspbian GNU/Linux 9.13 (Stretch)
배포판: Raspbian (Debian 기반)
버전: 9.13 (Stretch, 2017년 출시)
```



