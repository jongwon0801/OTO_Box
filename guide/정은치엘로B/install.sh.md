#### install.sh

```less
#!/bin/bash
if [ "$#" -lt 2 ]; then
    echo "$# is Illegal number of parameters."
    echo "Usage: $0 10000 lte"
    exit 1
fi
id=$1
if [ $2 == "lte" ]; then
  sudo sed -i '5,9s/#//g' /etc/iptables-hs
else
  sudo sed -i '5,9s/^/#/' /etc/iptables-hs 
fi

let z=$id+30000
sudo sed -i "s/.*/O2OBOX-${id}/" /etc/hostname
sudo sed -i "s/^127\.0\.0\.1.*O2OBOX.*/127.0.0.1 O2OBOX-${id}/" /etc/hosts
sudo sed -i "s/^RemoteForward.*localhost:8000$/RemoteForward  ${id} localhost:8000/" /root/.ssh/config
sed -i "s/^RemoteForward.*localhost:22$/RemoteForward  ${z} localhost:22/" .ssh/config
sudo sed -i "/^ssid=/ s/=.*/=오투오박스-${id}/" /etc/hostapd/hostapd.conf 
cd /home/pi/Workspace/appleapp/applelocker
/home/pi/.virtualenvs/o2obox/bin/python imp1.py "$id"
```

✅ 이 스크립트가 하는 일 요약
```less
입력값 확인: id와 lte 또는 wifi 같은 모드를 받음.

iptables 설정:

lte면 /etc/iptables-hs에서 주석 해제.

아니면 주석 처리.

호스트네임 설정:

/etc/hostname과 /etc/hosts에 O2OBOX-${id}로 설정.

SSH 리버스 터널 포트 수정:

.ssh/config 파일에서 RemoteForward 포트 수정.

와이파이 AP 이름 변경:

hostapd.conf에서 SSID를 오투오박스-${id}로 변경.

Python 스크립트 실행:

imp1.py 스크립트로 DB나 추가 설정 작업 수행.
```





