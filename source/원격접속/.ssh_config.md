#### Host와 HostName의 차이점

Host:

```less
Host는 SSH 설정의 이름 alias입니다. 즉, 사용자가 SSH 명령어에서 사용할 수 있는 이름입니다.

예를 들어, Host o2obox-tunnel을 정의하면, SSH 명령어에서 o2obox-tunnel을 호스트 이름으로 사용할 수 있습니다.

이것은 HostName에 정의된 실제 서버의 IP 주소나 도메인 이름과는 관계없습니다.
```

```less
Host o2obox-tunnel
    HostName server
    User root
    Port 2222
```
```less
위의 경우 Host가 o2obox-tunnel인 경우,
ssh o2obox-tunnel을 입력하면 HostName server에 정의된 server에 SSH 연결이 됩니다.
```

HostName:

```less
HostName은 실제로 SSH가 연결하려는 서버의 IP 주소 또는 도메인 이름입니다.

예를 들어, HostName server는 server라는 이름의 실제 호스트(도메인 또는 IP)로 SSH 연결을 시도하게 만듭니다.
만약 server가 ~/.ssh/config에 정의되지 않으면, server는 /etc/hosts나 DNS에서 IP를 찾아야 합니다.
```
```less
# HostName은 실제로 연결할 서버의 정보를 지정합니다.

Host o2obox-tunnel
    HostName server   # 실제 연결할 서버의 이름 또는 IP
    User root
    Port 2222
```


#### pi config 수정
```less
# sudo nano /home/pi/.ssh/config
# nano ~/.ssh/config

Host o2obox-ssh
HostName      server
User          root
Port          2222
IdentityFile  /home/pi/.ssh/id_rsa
#RemoteForward  11045 localhost:8000
RemoteForward  41045 localhost:22
ServerAliveInterval 300
ServerAliveCountMax 2
ExitOnForwardFailure yes
TCPKeepAlive yes
```

#### root config 수정
```less
# sudo nano /root/.ssh/config

Host o2obox-tunnel
HostName      server
User          root
Port          2222
IdentityFile  /home/pi/.ssh/id_rsa
RemoteForward  11045 localhost:8000
#RemoteForward  41045 localhost:22
ServerAliveInterval 300
ServerAliveCountMax 2
ExitOnForwardFailure yes
TCPKeepAlive yes
```
