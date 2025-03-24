

pgrep -af "ssh"

```
pgrep은 프로세스를 검색하는 명령으로, 특정 프로세스를 찾아 그 PID를 출력합니다.

-a 옵션은 프로세스 ID뿐만 아니라 프로세스의 전체 명령어 라인도 함께 출력하도록 합니다.

-f 옵션은 프로세스 명령어 라인에서 지정한 패턴을 검색하는 데 사용됩니다. 즉, "ssh"라는 패턴이 포함된 모든 프로세스를 출력합니다.

예를 들어, 이 명령은 현재 실행 중인 SSH 서버나 클라이언트 프로세스(예: sshd, ssh)의 PID와 명령어 라인 정보를 출력합니다.
```

ss -tp | grep ssh


```
ss는 네트워크 소켓 상태를 확인하는 명령입니다. ss는 netstat보다 더 빠르고 효율적입니다.

-t 옵션은 TCP 소켓만 표시하고, -p 옵션은 각 소켓에 관련된 프로세스를 표시합니다.

grep ssh는 ss 명령의 출력 중에서 "ssh"라는 문자열을 포함하는 부분만 필터링하여 표시합니다.
일반적으로 SSH 관련 포트(22번 포트)가 열려 있는 소켓 정보를 확인하는 데 사용됩니다.
```

#### crontab 리버스 ssh 주석 처리

```
sudo crontab -e

#@reboot /home/pi/reversesshservice.sh

sudo service cron restart
```




#### 로그 파일 삭제 후 재생성

```
# 기존 로그 파일 삭제 재생성
rm -f /home/pi/reversessh.log && touch /home/pi/reversessh.log

# 실행 권한 부여
chmod +x /home/pi/reversessh.sh

# 서비스 파일 생성
sudo nano /etc/systemd/system/reversessh.service
```

#### reversessh.service
```
[Unit]
Description=Reverse SSH Service
After=network.target

[Service]
ExecStart=/home/pi/reversessh.sh
Restart=always
User=pi
Environment=PATH=/usr/bin:/usr/sbin
WorkingDirectory=/home/pi
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
```

#### ssh 프로세스 죽이고 데몬 재실행
```
# 실행중인 프로세스 검색
pgrep -af "ssh"

1930 ssh -o ConnectTimeout=10 -f -N o2obox-tunnel

# 실행중인 리버스 ssh 종료
sudo kill -9 1930

# 데몬 재실행
sudo systemctl daemon-reload        # systemd가 새로운 서비스를 인식하도록 함

sudo systemctl enable reversessh.service  # 부팅 시 자동 실행 설정

sudo systemctl start reversessh.service   # 서비스 시작

sudo systemctl status reversessh.service  # 서비스 상태 확인

# 서비스 로그는 journalctl을 사용하여 확인
journalctl -u reversessh.service
```

#### 네이버 서버에서 listen 확인
```
# 원격접속
ssh -p 2222 root@smart.apple-box.kr

pw : tmshdnxmfl (스노우트리)

# listen 중인 포트 확인
netstat -tulnp | grep ssh

# 재실행한 yid 조회
netstat -tulnp | grep 11000
```


