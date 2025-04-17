#### 춘의동 세탁소(11013) pi 사용자 config

```less
192.168.0.164
/home/pi/.ssh/config

Host o2obox-ssh
  HostName      server
  User          root
  Port          2222
  IdentityFile  /home/pi/.ssh/id_rsa
  #RemoteForward  10000 localhost:8000
  RemoteForward  41001 localhost:22
  ServerAliveInterval 300
  ServerAliveCountMax 2
  ExitOnForwardFailure yes
  TCPKeepAlive yes
  StrictHostKeyChecking no

Host o2obox-vnc
  HostName      smart.apple-box.kr
  User          root
  Port          2222
  IdentityFile  /home/pi/.ssh/id_rsa
  RemoteForward  5900 localhost:5900
  ServerAliveInterval 300
  ServerAliveCountMax 2
  ExitOnForwardFailure yes
  TCPKeepAlive yes
  StrictHostKeyChecking no
```

#### 춘의동 세탁소(11013) root 사용자 config

```less
sudo su

/home/pi/.ssh/config

Host o2obox-ssh
  HostName      server
  User          root
  Port          2222
  IdentityFile  /home/pi/.ssh/id_rsa
  #RemoteForward  10000 localhost:8000
  RemoteForward  41001 localhost:22
  ServerAliveInterval 300
  ServerAliveCountMax 2
  ExitOnForwardFailure yes
  TCPKeepAlive yes
  StrictHostKeyChecking no
Host o2obox-vnc
  HostName      smart.apple-box.kr
  User          root
  Port          2222
  IdentityFile  /home/pi/.ssh/id_rsa
  RemoteForward  5900 localhost:5900
  ServerAliveInterval 300
  ServerAliveCountMax 2
  ExitOnForwardFailure yes
  TCPKeepAlive yes
  StrictHostKeyChecking no
```

#### /etc/hosts
```less
# /etc/hosts

127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
ff02::1         ip6-allnodes
ff02::2         ip6-allrouters

127.0.1.1               raspberrypi
127.0.0.1 O2OBOX-11013

125.209.200.159 vpnserver
10.100.80.100 homeserver
125.209.200.159 server
```












