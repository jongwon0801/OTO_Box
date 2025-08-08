#### 스마트도어 서버(centos 설치안되서 여기다함) 13.124.155.19

```less
# 서버 비밀키
server_private.key

iJeKJmenhVOXC4Oif/yIlZA+DoMLKeY/rsS60Ef+4lk=

# 서버 공개키 (클라이언트와 공유할 것)
server_public.key

ZsWlsY81Fc2DHaOHjfQizwr32bk32SbAere3YIDbFH4=
```

#### 클라이언트 비밀키 개인키

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
# wg-quick 서비스 상태 확인 (systemd 기반)
sudo systemctl status wg-quick@wg0

# WireGuard 인터페이스 상태 확인
sudo wg show

# 프로세스 시작
sudo wg-quick up wg0

# 이미 프로세스 올라와있으면 내리기
sudo wg-quick down wg0

# 자동으로 부팅 시 WireGuard가 시작
sudo systemctl enable wg-quick@wg0

# 서비스 수동 시작 시도
sudo systemctl start wg-quick@wg0
```



















