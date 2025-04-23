- pgrep -f -x 'ssh -o ConnectTimeout=10 -f -N o2obox-tunnel'

```
- ssh -o ConnectTimeout=10 -f -N o2obox-tunnel 프로세스가 실행 중인지 확인합니다.

- pgrep는 지정된 프로세스를 찾아 PID를 반환합니다.
```
<br>

- pgrep -af "ssh"

```
ssh 프로세스를 찾아 그 PID를 출력
```
<br>

- ps -aux | grep "ssh -o ConnectTimeout=10 -f -N o2obox-tunnel"

```
- ssh 명령이 실행 중인 모든 프로세스를 확인하고, 해당 프로세스가 포함된 정보를 출력합니다.

- grep으로 ssh 명령을 찾습니다.

pi        1840  0.0  0.0   6064   576 pts/0    S+   10:43   0:00 grep --color=auto ssh -o ConnectTimeout=10 -f -N o2obox-tunnel
root     23685  0.0  0.1  10616  1740 ?        Ss   06:51   0:00 ssh -o ConnectTimeout=10 -f -N o2obox-tunnel
```
<br>

- systemctl list-units --type=service | grep ssh
```
- 현재 실행 중인 서비스 중 ssh 관련 서비스를 목록화하고 출력합니다.

- SSH 서버 및 관련 서비스의 상태를 확인하는 데 유용합니다.

  reversessh.service                                          loaded active running Reverse SSH Service                                               
  ssh.service                                                 loaded active running OpenBSD Secure Shell server  
```
<br>

- systemctl show -p FragmentPath reversessh.service
```
- reversessh.service 서비스의 경로(FragmentPath)를 보여줍니다.

- 서비스의 구성 파일 위치를 확인하는 데 유용합니다.

FragmentPath=/lib/systemd/system/reversessh.service
```

<br>

- sudo find /etc/systemd /lib/systemd /usr/lib/systemd -name "reversessh.service"
```
- 시스템의 특정 디렉토리에서 reversessh.service 파일을 검색합니다.

- 서비스 파일의 위치를 확인할 수 있습니다.

/etc/systemd/system/multi-user.target.wants/reversessh.service
/lib/systemd/system/reversessh.service
```

<br>

- systemctl status reversessh.service
```
- reversessh.service의 현재 상태를 확인합니다.
```

<br>

- ls -l /etc/systemd/system/multi-user.target.wants/reversessh.service
```
- reversessh.service가 multi-user.target에서 활성화되어 있는지 확인합니다.

- 해당 서비스가 현재 multi-user.target에서 링크되어 있는지 보여줍니다.

lrwxrwxrwx 1 root root 38  3월 12  2020 /etc/systemd/system/multi-user.target.wants/reversessh.service -> /lib/systemd/system/reversessh.service
```

- sudo nano /lib/systemd/system/reversessh.service

- reversessh.service의 실제 시스템 서비스 파일을 수정합니다.

- 이 파일에서 서비스 실행 명령과 설정을 변경할 수 있습니다.
<br>

```
[Unit]
Description=Reverse SSH Service
After=network.target

[Service]
Type=idle
ExecStart=/bin/sh /home/pi/reversesshservice.sh

[Install]
WantedBy=multi-user.target
```
<br>

1️⃣ 기존 enable된 파일 삭제 후 다시 설정
```
# 기존 심볼릭 링크 제거
sudo rm /etc/systemd/system/multi-user.target.wants/reversessh.service

# daemon-reload로 systemd 캐시 갱신
sudo systemctl daemon-reload

# 다시 enable 실행
sudo systemctl enable reversessh.service

sudo systemctl start reversessh.service

sudo systemctl status reversessh.service
```
<br>
2️⃣ 심볼릭 링크 확인 및 재생성 (만약 직접 수정하고 싶다면)

- 심볼릭 링크가 올바르게 /lib/systemd/system/reversessh.service를 가리키는지 확인.
ls -l /etc/systemd/system/multi-user.target.wants/reversessh.service

<br>

만약 링크가 잘못되었거나 깨졌다면 수동으로 다시 생성
sudo ln -s /lib/systemd/system/reversessh.service /etc/systemd/system/multi-user.target.wants/reversessh.service
<br>

<br>
✅ 1. /lib/systemd/system/은 "기본 서비스 파일"이 저장되는 곳
/lib/systemd/system/ 경로는 패키지 설치 시 기본 서비스 파일을 저장하는 곳

예를 들어, apt install openssh-server 하면 ssh.service가 /lib/systemd/system/에 저장됨

🔹 즉, 공식 서비스 파일은 /lib/systemd/system/에 위치해야 한다!


- ls /lib/systemd/system/ | grep ssh
<br>



✅ 2. /etc/systemd/system/multi-user.target.wants/는 실행될 서비스 목록을 저장하는 곳
systemctl enable 서비스명을 실행하면
→ /etc/systemd/system/multi-user.target.wants/에 해당 서비스의 심볼릭 링크가 생성됨

즉, 여기 있는 서비스들은 부팅 시 자동 실행됨


🔹 "이 서비스는 부팅 시 실행해야 해!"라는 걸 systemd가 알도록 하기 위해 심볼릭 링크를 생성하는 것!

#### 심볼릭 링크인지 확인 앞에 l 붙었으면 심볼릭 링크
- ls -l /etc/systemd/system/multi-user.target.wants/reversessh.service
<br>

#### 심볼링 링크 enable/disable 상태를 바로 확인
sudo systemctl is-enabled reversessh.service

<br>

#### 서비스 만든 후 안될 경우

```
sudo systemctl start reversessh.service

sudo systemctl status reversessh.service
```

#### 1. knownhosts 제거
```
cd ~/.ssh

sudo nano known_hosts

# 서버 재연결로 knownhosts 추가
ssh -p 2222 root@smart.apple-box.kr
```

#### 2. 로그파일 권한 부여
```
./reversesshservice.sh 실행 해보고 오류 확인

ls -l /home/pi/reversessh.log

sudo chmod 666 /home/pi/reversessh.log
```

#### 3. RSA root 키 복사
```
sudo mkdir -p /root/.ssh

sudo chmod 700 /root/.ssh
```

- mkdir -p /root/.ssh → .ssh 폴더가 없으면 생성

- chmod 700 /root/.ssh → root만 접근 가능하도록 권한 설정

```
# pi 계정의 SSH 키를 root 계정으로 복사

sudo cp /home/pi/.ssh/id_rsa /root/.ssh/id_rsa

sudo cp /home/pi/.ssh/id_rsa.pub /root/.ssh/id_rsa.pub
```

```
sudo chmod 600 /root/.ssh/id_rsa

sudo chmod 644 /root/.ssh/id_rsa.pub
```

- chmod 600 id_rsa → 개인 키는 root만 읽고 쓸 수 있도록 설정

- chmod 644 id_rsa.pub → 공개 키는 읽기 가능

#### 4. 설정 확인
```
sudo ls -l /root/.ssh/

-rw------- 1 root root  3243  4월  2 12:34 id_rsa
-rw-r--r-- 1 root root   745  4월  2 12:34 id_rsa.pub
```

#### 5. 안되면 기존 키 삭제 후 변경
```
# smart.apple-box.kr:2222 기존 root SSH 키를 삭제
sudo ssh-keygen -f "/root/.ssh/known_hosts" -R "[smart.apple-box.kr]:2222"

# tunnel.o2obox.kr:2222의 기존 root SSH 키를 삭제
sudo ssh-keygen -f "/root/.ssh/known_hosts" -R "[tunnel.o2obox.kr]:2222"
```

#### 6. 호스트 키를 다시 등록하기 위해 직접 SSH 접속을 시도
```
sudo ssh -i /root/.ssh/id_rsa -p 2222 smart.apple-box.kr

sudo ssh -i /root/.ssh/id_rsa -p 2222 tunnel.o2obox.kr

# 재시작
sudo systemctl restart reversessh.service
```

#### lsof -> ss ,호스트키 변경 방지 수정 reversesshservice.sh
```
serverProcessKill() {
    export IFS="-"
    sentence="$(hostname)"

    for word in $sentence; do
        yid="$word"
    done

    if [ -n "$yid" ]; then
        echo "Trying to kill process using port $yid on server..."
        ssh -T -p 2222 root@server "kill -9 \$(lsof -ti tcp:$yid) || echo 'No process found using port $yid'"
    else
        echo "Invalid port extracted from hostname."
    fi
}

startSsh(){
    pid="$(ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -f -N o2obox-tunnel 2>&1)"
    if [ "$?" -ne 0 ]; then
        log "$pid"
    fi
}

getSshProcess(){
    pid="$(pgrep -f -x 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -f -N o2obox-tunnel')"
}

stopSsh(){
    pid="$(pgrep -f -x 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -f -N o2obox-tunnel')"
    if [ "$pid" != ""  ]; then
        log "stop ssh"
        kill "$pid"
    fi
}

initIp(){
    systemctl restart dhcpcd.service
}

startReverseSsh(){
    serverProcessKill

    if [ "$?" -eq 0 ]; then
        startSsh
        if [ "$?" -eq 0 ]; then
            log "success reverse ssh"
        else
            log "server connection error because of sshstart"
        fi
    else
        log "no server kill"
        startSsh
        if [ "$?" -eq 0 ]; then
            log "success reverse ssh"
        else
            log "server connection error because of sshstart"
        fi
    fi
}

getIp(){
    ip="$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)"
}

log(){
    echo "$1"
    echo "Time: $(date) $1" >> /home/pi/reversessh.log
}

log "start daemon"
while true; do
    getIp

    if [ "$ip" = "" ]; then
        log "no ip"
        initIp
        stopSsh
        sleep 10
    else
        getSshProcess
        if [ "$pid" = "" ]; then
            startReverseSsh
            log "start ssh"
            sleep 20
        else
            sleep 20
        fi
    fi
done
```


---
#### 시스템 재실행시 reversesshservice.sh 실행 가능 옵션

```
/etc/rc.local: 시스템 시작 시 실행될 스크립트를 추가할 수 있습니다.

/etc/systemd/system/: 서비스 파일을 추가하여 자동 시작하도록 설정합니다.

crontab: @reboot 명령을 사용하여 시스템 시작 시 실행되도록 설정할 수 있습니다.
```



#### /etc/hosts 수정

- 시스템에서 특정 호스트 이름을 IP 주소에 매핑할 때 사용되는 /etc/hosts 파일을 수정합니다.

- 이 파일을 수정하면 도메인 이름을 로컬에서 특정 IP로 직접 매핑할 수 있습니다.


- sudo systemctl restart networking

- 네트워크 서비스를 재시작하여 네트워크 설정을 적용합니다.

- 네트워크 설정 파일을 수정한 후 이 명령을 사용하여 변경 사항을 적용합니다.

- 네트워크 연결 상태를 확인

```
ping localhost
ping -c 3 10.100.80.100
ping -c 3 125.209.200.159
```
- -c 3은 3번만 ping을 보내는 옵션
- localhost는 자신을 나타내는 IP 주소인 127.0.0.1



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

sudo systemctl disable reversessh.service  # 서비스 비활성화 (부팅 시 자동 실행 해제)

sudo systemctl stop reversessh.service    # 실행 중인 서비스 중지 (즉시 종료)

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
netstat -tulnp | grep 11013
```

