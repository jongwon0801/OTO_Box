#### 원격 접속

```less
# 전역 SSH 설정 파일
/etc/ssh
~/.ssh/config 처럼 사용자 개별이 아닌, 시스템 전체에 적용되는 설정

~/.ssh/config

# iptable 조회
sudo iptables -L -n

# 포트 설정조회
/etc/ssh/sshd_config
```

#### 아이비힐 (o2obox) pi@O2OBOX-11000:~ $ sudo iptables -L -n

```less
Chain INPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  125.209.200.159      0.0.0.0/0           
ACCEPT     all  --  211.233.84.186       0.0.0.0/0           
DROP       all  --  0.0.0.0/0            0.0.0.0/0           

Chain FORWARD (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0            state RELATED,ESTABLISHED
ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0           

Chain OUTPUT (policy ACCEPT)
target     prot opt source               destination         
ACCEPT     all  --  0.0.0.0/0            125.209.200.159     
ACCEPT     all  --  0.0.0.0/0            211.233.84.186      
DROP       all  --  0.0.0.0/0            0.0.0.0/0      
```

#### 문제 있는 11040의 경우

```less
INPUT:
ACCEPT all -- 125.209.200.159 0.0.0.0/0
DROP   all -- 0.0.0.0/0       0.0.0.0/0


OUTPUT:
ACCEPT all -- 0.0.0.0/0 125.209.200.159
DROP   all -- 0.0.0.0/0 0.0.0.0/0
```

#### 여기서는 서버 이외에 어떤 IP도 허용 안 함

```less
서버에서 reverse ssh 열고 나서 localhost:11040을 외부에서 접근할 수 있도록 바인딩 했다 해도,
클라이언트 쪽에서 iptables이 막고 있으니, 접속 자체가 DROP되는 상황
```






