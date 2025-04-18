#### 네트워크 설정 

```less
파일을 수정하여 AP의 설정을 관리, 비밀번호를 설정 가능

sudo nano /etc/hostapd/hostapd.conf


hostapd를 시스템이 부팅할 때 자동으로 시작되도록 하려면 서비스 파일을 설정

sudo nano /etc/default/hostapd


/etc/dnsmasq.conf 파일을 수정하여 DHCP 서버를 설정

sudo nano /etc/dnsmasq.conf


AP 장치(예: 라즈베리파이)의 고정 IP 설정
/etc/dhcpcd.conf
```
