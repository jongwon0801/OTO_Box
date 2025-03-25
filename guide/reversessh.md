#### ssh가 실행되고 있는지 확인

pgrep -f -x 'ssh -o ConnectTimeout=10 -f -N o2obox-tunnel'


systemctl status reversessh.service


/etc/hosts 수정

```
127.0.0.1       localhost O2OBOX-11013
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

# 로컬 호스트명
127.0.0.1       raspberrypi

# 서버 IP 설정 (중복 제거)
10.100.80.100   homeserver
125.209.200.159 vpnserver server

```

sudo systemctl restart networking




ping localhost
ping -c 3 10.100.80.100
ping -c 3 125.209.200.159
