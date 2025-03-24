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

