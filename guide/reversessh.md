#### ssh가 실행되고 있는지 확인
```
pgrep -f -x 'ssh -o ConnectTimeout=10 -f -N o2obox-tunnel'

ps -aux | grep "ssh -o ConnectTimeout=10 -f -N o2obox-tunnel"

pi        1840  0.0  0.0   6064   576 pts/0    S+   10:43   0:00 grep --color=auto ssh -o ConnectTimeout=10 -f -N o2obox-tunnel
root     23685  0.0  0.1  10616  1740 ?        Ss   06:51   0:00 ssh -o ConnectTimeout=10 -f -N o2obox-tunnel

sudo cat /etc/systemd/system/* | grep "o2obox-tunnel"

systemctl list-units --type=service | grep ssh
  reversessh.service                                          loaded active running Reverse SSH Service                                               
  ssh.service                                                 loaded active running OpenBSD Secure Shell server  


systemctl show -p FragmentPath reversessh.service
FragmentPath=/lib/systemd/system/reversessh.service

sudo find /etc/systemd /lib/systemd /usr/lib/systemd -name "reversessh.service"
/etc/systemd/system/multi-user.target.wants/reversessh.service
/lib/systemd/system/reversessh.service

systemctl status reversessh.service

ls -l /etc/systemd/system/multi-user.target.wants/reversessh.service
lrwxrwxrwx 1 root root 38  3월 12  2020 /etc/systemd/system/multi-user.target.wants/reversessh.service -> /lib/systemd/system/reversessh.service



```

#### sudo nano /etc/systemd/system/multi-user.target.wants/reversessh.service

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


#### sudo nano /lib/systemd/system/reversessh.service

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


#### 시스템 재실행시 reversesshservice.sh 실행 가능 옵션

```
sudo cat /etc/rc.local

/etc/systemd/system/  service 파일

sudo crontab -e
```


/etc/hosts 수정


sudo systemctl restart networking


ping localhost
ping -c 3 10.100.80.100
ping -c 3 125.209.200.159







