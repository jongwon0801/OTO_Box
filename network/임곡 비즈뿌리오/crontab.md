#### 크론탭 조회
```less
(o2obox) pi@O2OBOX-20001:~/Downloads/config $ sudo crontab -l
```

#### sudo crontab -e
```less
# Edit this file to introduce tasks to be run by cron.
# 
# Each task to run has to be defined through a single line
# indicating with different fields when the task will be run
# and what command to run for the task
# 
# To define the time you can provide concrete values for
# minute (m), hour (h), day of month (dom), month (mon),
# and day of week (dow) or use '*' in these fields (for 'any').
# 
# Notice that tasks will be started based on the cron's system
# daemon's notion of time and timezones.
# 
# Output of the crontab jobs (including errors) is sent through
# email to the user the crontab file belongs to (unless redirected).
# 
# For example, you can run a backup of all your user accounts
# at 5 a.m every week with:
# 0 5 * * 1 tar -zcf /var/backups/home.tgz /home/
# 
# For more information see the manual pages of crontab(5) and cron(8)
# 
# m h  dom mon dow   command
0 4 * * 6 /sbin/shutdown -r now # 매일 새벽 4시에 실행
#@reboot /home/pi/reversesshservice.sh
#0 0 * * 0 ntpdate -u 211.233.84.186
#0 0 * * 0 ntpdate -u server
@reboot /opt/pprio/script/biz_start
* * * * * sudo hcitool -i hci0 cmd 0x08 0x0008 1E 02 01 06 1A FF 4C 00 02 15 C7 C1 A1 BF BB 00 4C AD 87 04 9F 2D 29 17 DE D2 00 00 00 00 C8 00
```


