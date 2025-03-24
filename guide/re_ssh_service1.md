

pgrep -af "ssh":

```
pgrep은 프로세스를 검색하는 명령으로, 특정 프로세스를 찾아 그 PID를 출력합니다.

-a 옵션은 프로세스 ID뿐만 아니라 프로세스의 전체 명령어 라인도 함께 출력하도록 합니다.

-f 옵션은 프로세스 명령어 라인에서 지정한 패턴을 검색하는 데 사용됩니다. 즉, "ssh"라는 패턴이 포함된 모든 프로세스를 출력합니다.

예를 들어, 이 명령은 현재 실행 중인 SSH 서버나 클라이언트 프로세스(예: sshd, ssh)의 PID와 명령어 라인 정보를 출력합니다.
```

ss -tp | grep ssh:


```
ss는 네트워크 소켓 상태를 확인하는 명령입니다. ss는 netstat보다 더 빠르고 효율적입니다.

-t 옵션은 TCP 소켓만 표시하고, -p 옵션은 각 소켓에 관련된 프로세스를 표시합니다.

grep ssh는 ss 명령의 출력 중에서 "ssh"라는 문자열을 포함하는 부분만 필터링하여 표시합니다.
일반적으로 SSH 관련 포트(22번 포트)가 열려 있는 소켓 정보를 확인하는 데 사용됩니다.
```

#### 라즈베리 파이에서 autossh 설치

```
# 라즈베리 파이의 패키지 목록을 업데이트
sudo apt update

# autossh 설치
sudo apt install autossh

# 버젼 확인
autossh -V
```

#### autossh 설정 및 사용

```
autossh -M 0 -f -N -R [외부서버포트]:localhost:22 [사용자명]@[서버IP]

-M 0: 모니터링 포트를 사용하지 않음
-f: 백그라운드로 실행
-N: 명령어를 실행하지 않고 연결만 유지
-R [포트]: 외부 서버에서 라즈베리 파이의 포트를 열어줌
```

#### autossh -M 0 -f -N -R 11000:localhost:22 pi@smart.apple-box.kr


#### 서비스 파일 생성
```
sudo nano /etc/systemd/system/autossh.service
```

#### autossh.service
```
[Unit]
Description=AutoSSH Service for Reverse SSH
After=network.target

[Service]
ExecStart=/usr/bin/autossh -M 0 -f -N -R 11000:localhost:22 pi@smart.apple-box.kr
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```

#### 서비스 리로드 및 시작
```
sudo systemctl daemon-reload
sudo systemctl start autossh.service
sudo systemctl enable autossh.service
```

