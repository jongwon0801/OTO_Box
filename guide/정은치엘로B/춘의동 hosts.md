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








