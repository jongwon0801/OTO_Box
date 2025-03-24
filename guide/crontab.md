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
