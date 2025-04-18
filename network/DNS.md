🔹 /etc/resolv.conf

➡️ 시스템 전체에서 참조하는 DNS 설정 파일
➡️ ping google.com 같은 명령이 참조함
➡️ 여기에 nameserver 127.0.0.1 이렇게 써 있으면, 로컬 DNS 서버(dnsmasq 등)를 사용한다는 의미

🔸 /run/dnsmas/resolv.conf

➡️ dnsmasq가 참조하는 “외부 DNS 서버 목록”
➡️ dnsmasq는 이걸 보고 "내가 127.0.0.1에서 받은 DNS 요청을 어디로 넘길까?"를 결정함


💡 연결 고리
/etc/resolv.conf → 127.0.0.1 설정됨

127.0.0.1 포트 53에는 dnsmasq가 동작 중

dnsmasq는 /run/dnsmas/resolv.conf 보고 외부 DNS로 쿼리 넘김
👉 근데 /run/dnsmas/resolv.conf가 잘못됐거나 없으면 외부 연결 안 됨


/run/dnsmasq/resolv.conf

```less
nameserver 168.126.63.1
nameserver 168.126.63.2
```

이건 KT DNS 서버 (한국에서 일반적으로 사용하는)
즉, dnsmasq는 외부 DNS 서버로 요청을 넘길 준비가 돼 있음.
이론적으로는 도메인 해석 문제 없어야 함

---

#### iptables 확인 (방화벽 문제 확인)
```less
sudo iptables -L -n -v
``` 
iptables에서 eth0 인터페이스로 나가는 모든 트래픽이 차단(DROP) 되어 있음

```less
Chain OUTPUT (policy ACCEPT 9835 packets, 736K bytes)
...
DROP       all  --  *      eth0    0.0.0.0/0            0.0.0.0/0
```

그리고 INPUT에도 eth0으로 들어오는 거 다 막고 있음

```less
Chain INPUT
...
DROP       all  --  eth0   *       0.0.0.0/0            0.0.0.0/0
```

iptables 규칙 초기화 (일단 다 허용)
```less
sudo iptables -F
sudo iptables -X
sudo iptables -t nat -F
sudo iptables -t nat -X
```









