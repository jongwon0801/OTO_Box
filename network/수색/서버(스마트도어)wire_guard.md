#### 스마트도어 서버(centos 설치안되서 여기다함) 13.124.155.19

```less
# 서버 비밀키
server_private.key

iJeKJmenhVOXC4Oif/yIlZA+DoMLKeY/rsS60Ef+4lk=

# 서버 공개키 (클라이언트와 공유할 것)
server_public.key

ZsWlsY81Fc2DHaOHjfQizwr32bk32SbAere3YIDbFH4=
```

#### 클라이언트(전시회문) 비밀키 개인키

```less
# 클라이언트 비밀키
client_private.key

MBhclr0aZ9vPTdJQJySHx8UhLZny9bds34CY4n6OOlM=

# 클라이언트 공개키 (서버에 알려줘야 함)
client_public.key

FSNL9nRwIW63v1TN9CC6r8ia+3XsPZpMY94gUK83uDc=
```

#### 프로세스 상태 확인

```less
# WireGuard 인터페이스 상태 확인
sudo wg show

ip addr show wg0

# 프로세스 시작
sudo wg-quick up wg0

# 이미 프로세스 올라와있으면 내리기
sudo wg-quick down wg0
```

#### system 프로세스 시작 중지
```less
# 자동으로 부팅 시 WireGuard가 시작
sudo systemctl enable wg-quick@wg0

# wg-quick 서비스 상태 확인 (systemd 기반)
sudo systemctl status wg-quick@wg0

# 서비스 중지
sudo systemctl stop wg-quick@wg0

# 서비스 시작
sudo systemctl start wg-quick@wg0
```

#### 패킷 보내기 테스트
```less
# iptables 규칙확인
sudo iptables -L -n -v

sudo iptables -A INPUT -p udp --dport 51820 -j ACCEPT

sudo iptables -D INPUT -p udp --dport 51820 -j ACCEPT

# 서버 패킷 51820 포트로 받을준비
sudo tcpdump -i any udp port 51820

# 클라이언트 패킷 보내기 설치
sudo apt update
sudo apt install netcat

echo "hello" | nc -u 13.124.155.19 51820
```

#### IP 포워딩 활성화 확인
```less
sudo sysctl net.ipv4.ip_forward

1이어야 정상 작동

0이라면

sudo sysctl -w net.ipv4.ip_forward=1


영구 반영하려면 /etc/sysctl.conf에 net.ipv4.ip_forward=1 추가
```

#### 서버 wg0.conf
```less
[Interface]
Address = 10.0.0.1/24         # 서버 VPN 내부 IP
ListenPort = 51820            # 기본 WireGuard 포트 (UDP)
PrivateKey = iJeKJmenhVOXC4Oif/yIlZA+DoMLKeY/rsS60Ef+4lk=

# 이후 클라이언트 연결할 때 [Peer] 섹션 추가
[Peer]
PublicKey = FSNL9nRwIW63v1TN9CC6r8ia+3XsPZpMY94gUK83uDc=
AllowedIPs = 10.0.0.2/32
```

#### 클라이언트 wg0.conf
```less
[Interface]
PrivateKey = MBhclr0aZ9vPTdJQJySHx8UhLZny9bds34CY4n6OOlM=    # 클라이언트_비밀키_내용
Address = 10.0.0.2/32          # 클라이언트의 VPN 내부 IP (서버와 같은 대역)
DNS = 8.8.8.8

[Peer]
PublicKey = ZsWlsY81Fc2DHaOHjfQizwr32bk32SbAere3YIDbFH4=    # 서버_공개키_내용
Endpoint = 13.124.155.19:51820                            # 서버_퍼블릭_IP:51820
AllowedIPs = 10.0.0.1/32
PersistentKeepalive = 25
```





