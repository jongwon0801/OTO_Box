#### 크론탭 관련 명령

```
crontab -l : 현재 사용자의 크론 작업을 확인합니다.

crontab -e : 현재 사용자의 크론 작업을 편집합니다.

sudo crontab -l : 루트 사용자의 크론 작업을 확인합니다.

sudo crontab -e : 루트 사용자의 크론 작업을 편집합니다.
```


#### 사용자(pi)의 Cron 작업
```
0 2 * * * cd /home/pi/Workspace/appleapp/applelocker && /home/pi/.virtualenvs/o2obox/bin/python syncdb_rfid.py
3 3 * * * cd /home/pi/Workspace/appleapp/applelocker && /home/pi/.virtualenvs/o2obox/bin/python export.py -t locker
```


#### 루트(sudo crontab)의 Cron 작업
```
0 4 * * 6 /sbin/shutdown -r now # 매주 토요일 새벽 4시에 서버 재부팅
@reboot /opt/pprio/script/biz_start # 시스템 부팅 시 실행
* * * * * sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 06 1A FF 4C 00 02 15 C7 C1 A1 BF BB 00 4C AD 87 04 9F 2D 29
17 DE D2 00 00 00 00 C8 00 # 매분마다 블루투스 명령 실행
```

#### 리버스 ssh 재시작시 자동 연결
```
# 주석해제
#@reboot /home/pi/reversesshservice.sh

# 크론탭 수정 후 재시작
sudo service cron restart
or sudo reboot
```

#### 권한 조회
```
ls -l /home/pi/reversesshservice.sh

-rwxr-xr-x 1 pi pi 1871 11월 27  2020 /home/pi/reversesshservice.sh

# 권한 없으면 권한 부여
chmod +x reversesshservice.sh 명령어를 실행하면 소유자(owner), 그룹(group), 다른 사용자(other) 모두에게 실행 권한이 추가

# 리버스 ssh 재실행
./reversesshservice.sh
```

#### 서버에서 터널 확인
```
# 원격접속
ssh -p 2222 root@smart.apple-box.kr

pw : tmshdnxmfl (스노우트리)

# listen 중인 포트 확인
netstat -tulnp | grep ssh

netstat -tulnp | grep ':11000'
```





