#### iptables 설정

```less
# nano /etc/iptables-hs

#!/bin/bash
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT
# 서버와의 통신만 허용함 (LTE라우터인 경우)
#iptables -A INPUT -s 125.209.200.159 -j ACCEPT
#iptables -A OUTPUT -d 125.209.200.159 -j ACCEPT
#iptables -A OUTPUT -o eth0 -j DROP
#iptables -A INPUT -i eth0 -j DROP
```


```less
#!/bin/bash

# NAT 설정: eth0 인터페이스를 통해 나가는 트래픽에 대해 주소 변환(Masquerading) 수행
# -t nat: NAT 테이블을 사용
# -A POSTROUTING: 패킷이 시스템을 떠날 때 적용할 규칙을 추가
# -o eth0: eth0 인터페이스에서 나가는 패킷에 적용
# -j MASQUERADE: 출발지 IP 주소를 변경하여 내부 네트워크의 IP 주소를 숨김
iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE

# eth0에서 wlan0으로 가는 패킷을 포워딩하는 규칙 설정
# -A FORWARD: 포워딩 규칙을 추가
# -i eth0 -o wlan0: eth0에서 wlan0으로 가는 패킷을 처리
# -m state --state RELATED,ESTABLISHED: 이미 연결된 세션의 패킷만 허용
# -j ACCEPT: 해당 패킷을 허용
iptables -A FORWARD -i eth0 -o wlan0 -m state --state RELATED,ESTABLISHED -j ACCEPT

# wlan0에서 eth0으로 가는 패킷을 포워딩하는 규칙 설정
# -A FORWARD: 포워딩 규칙을 추가
# -i wlan0 -o eth0: wlan0에서 eth0으로 가는 패킷을 처리
# -j ACCEPT: 해당 패킷을 허용
iptables -A FORWARD -i wlan0 -o eth0 -j ACCEPT

# 아래 주석 처리된 규칙들은 특정 IP와의 통신을 허용하거나 차단하기 위한 예시입니다.
# LTE 라우터와의 통신만 허용하는 규칙들 (필요한 경우 활성화)
# 서버와의 통신만 허용하기 위한 설정 (특정 IP와의 연결만 허용)
# 특정 IP 주소(125.209.200.159)에서 오는 패킷을 허용
#iptables -A INPUT -s 125.209.200.159 -j ACCEPT

# 특정 IP 주소(125.209.200.159)로 나가는 패킷을 허용
#iptables -A OUTPUT -d 125.209.200.159 -j ACCEPT

# eth0 인터페이스를 통해 나가는 모든 출력 패킷을 차단
#iptables -A OUTPUT -o eth0 -j DROP

# eth0 인터페이스를 통해 들어오는 모든 입력 패킷을 차단
#iptables -A INPUT -i eth0 -j DROP
```

```less
# /etc/systemd/system/hs-iptables.service

[Unit]
Description=Activate IPtables for Hotspot
After=network-pre.target
Before=network-online.target

[Service]
Type=simple
ExecStart=/etc/iptables-hs

[Install]
WantedBy=multi-user.target
```

```less
sudo systemctl daemon-reload

# 서비스 enable 시 심링크 생성됨
sudo systemctl enable hs-iptables.service

sudo systemctl start hs-iptables.service

sudo systemctl status hs-iptables.service

Active: inactive (dead):

Type=simple + 명령어가 금방 끝나는 구조이기 때문에,

iptables 명령만 실행하고 종료되었음 (정상임)

status=0/SUCCESS: 성공적으로 실행되었단 뜻! 문제 없음
```


```less
# /etc/systemd/system/multi-user.target.wants/hs-iptables.service

[Unit]
Description=Activate IPtables for Hotspot          # 서비스 설명
After=network-pre.target                           # 네트워크 초기화 이전에 실행되면 안 됨
Before=network-online.target                       # 네트워크가 완전히 연결되기 전에 실행되어야 함

[Service]
Type=simple                                         # 단순한 실행형 서비스 (백그라운드로 계속 안 돌고, 한번 실행)
ExecStart=/etc/iptables-hs                         # 실행할 스크립트 경로 (/etc/iptables-hs)

[Install]
WantedBy=multi-user.target                         # 일반 사용자 환경 진입할 때 실행됨
```

✅ .service 파일을 /etc/systemd/system/에 만든 경우
```less
systemd는 기본적으로 아래 경로들을 다 검색해:

/lib/systemd/system/ (패키지 설치 시 기본 위치)

/etc/systemd/system/ (사용자가 직접 만든 커스텀 서비스 위치)
```
