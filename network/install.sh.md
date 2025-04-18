#### install.sh

```less
# 주석 제거 -> 서버 이외의 인터넷 접속 제한
install.sh 11040 lte

# 주석 추가 -> 인터넷 제한 X
install.sh 11040 wifi
```

```less
#!/bin/bash

# 인자 개수가 2개 미만이면 에러 메시지 출력 후 종료
if [ "$#" -lt 2 ]; then
    echo "$# is Illegal number of parameters."
    echo "Usage: $0 10000 lte"
    exit 1
fi

# 첫 번째 인자를 id 변수에 저장 (예: 10000)
id=$1

# 두 번째 인자가 "lte"이면 iptables-hs 파일의 5~9번째 줄에서 주석 제거
if [ $2 == "lte" ]; then
  sudo sed -i '5,9s/#//g' /etc/iptables-hs
else
  # lte가 아니면 해당 줄에 주석(#) 추가
  sudo sed -i '5,9s/^/#/' /etc/iptables-hs 
fi

# id에 30000을 더한 값을 z 변수에 저장 (예: 10000 → 40000)
let z=$id+30000

# 호스트네임 변경 (예: O2OBOX-10000)
sudo sed -i "s/.*/O2OBOX-${id}/" /etc/hostname

# /etc/hosts 파일의 호스트네임 줄도 동일하게 변경
sudo sed -i "s/^127\.0\.0\.1.*O2OBOX.*/127.0.0.1 O2OBOX-${id}/" /etc/hosts

# root 계정의 ssh 설정에서 reverse tunnel 포트(8000 → ID) 변경
sudo sed -i "s/^RemoteForward.*localhost:8000$/RemoteForward  ${id} localhost:8000/" /root/.ssh/config

# pi 계정의 ssh 설정에서 reverse tunnel 포트(22 → ID+30000) 변경
sed -i "s/^RemoteForward.*localhost:22$/RemoteForward  ${z} localhost:22/" .ssh/config

# AP 이름(SSID)을 "오투오박스-<id>"로 변경
sudo sed -i "/^ssid=/ s/=.*/=오투오박스-${id}/" /etc/hostapd/hostapd.conf 

# 작업 디렉토리로 이동
cd /home/pi/Workspace/appleapp/applelocker

# 가상환경에서 imp1.py 파이썬 스크립트 실행 (ID를 인자로 전달)
# → 예: python imp1.py 10000
/home/pi/.virtualenvs/o2obox/bin/python imp1.py "$id"

```

🔧 스크립트 전체 요약

$1 = ID 값 (예: 10000)

$2 = 접속 모드 (lte 또는 다른 것)

ID 기반으로

- iptables 설정 파일 제어

- 호스트 이름 변경

- SSH reverse tunnel 포트 설정

- hostapd SSID 변경

- 파이썬 스크립트 실행












