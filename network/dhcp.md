#### 1. dhcpcd 서비스 (DHCP 클라이언트)

```less
/etc/systemd/system/multi-user.target.wants/dhcpcd.service

[Unit]
Description=dhcpcd on all interfaces
Wants=network.target
Before=network.target

[Service]
Type=forking
PIDFile=/run/dhcpcd.pid
ExecStart=/usr/lib/dhcpcd5/dhcpcd -q -b
ExecStop=/sbin/dhcpcd -x

[Install]
WantedBy=multi-user.target
Alias=dhcpcd5.service
```


2. dnsmasq 서비스 (DHCP + DNS 서버)

```less
/etc/systemd/system/multi-user.target.wants/dhcpcd.service

[Unit]
Description=dnsmasq - A lightweight DHCP and caching DNS server
Requires=network.target
Wants=nss-lookup.target
Before=nss-lookup.target
After=network.target

[Service]
Type=forking
PIDFile=/run/dnsmasq/dnsmasq.pid
ExecStartPre=/usr/sbin/dnsmasq --test
ExecStart=/etc/init.d/dnsmasq systemd-exec
ExecStartPost=/etc/init.d/dnsmasq systemd-start-resolvconf
ExecStop=/etc/init.d/dnsmasq systemd-stop-resolvconf
ExecReload=/bin/kill -HUP $MAINPID

[Install]
WantedBy=multi-user.target
```

#### AP모드 와이파이 비밀번호 설정

sudo nano /etc/hostapd/hostapd.conf






