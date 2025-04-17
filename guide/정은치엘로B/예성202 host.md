#### 예성 202 host

```less
(o2obox) pi@O2OBOX-11010:~ $ cat /etc/hosts
127.0.0.1	localhost
::1		localhost ip6-localhost ip6-loopback
ff02::1		ip6-allnodes
ff02::2		ip6-allrouters

127.0.0.1 O2OBOX-11010
125.209.200.159 server
#192.168.0.6 server
#125.209.200.159 smart.apple-box.kr
```
```less
# pi 사용자 config

(o2obox) pi@O2OBOX-11010:~/.ssh $ cat config 
Host o2obox-ssh
HostName      server
User          root
Port          2222
IdentityFile  /home/pi/.ssh/id_rsa
#RemoteForward  10000 localhost:8000
RemoteForward 41010  localhost:22
ServerAliveInterval 300
ServerAliveCountMax 2
ExitOnForwardFailure yes
TCPKeepAlive yes
```

```less
# root 사용자 config

sudo su

root@O2OBOX-11010:/home/pi/.ssh# cat config 
Host o2obox-ssh
HostName      server
User          root
Port          2222
IdentityFile  /home/pi/.ssh/id_rsa
#RemoteForward  10000 localhost:8000
RemoteForward 41010  localhost:22
ServerAliveInterval 300
ServerAliveCountMax 2
ExitOnForwardFailure yes
TCPKeepAlive yes
```
