#### 네트워크, SELinux, 방화벽 임시 비활성화
```less
# SELinux는 비활성화
sudo setenforce 0

# 방화벽 임시 비활성화
sudo systemctl stop firewalld
```


#### 캐시 및 잠금 파일 수동 삭제
```less
sudo rm -f /var/run/yum.pid /var/run/yum.pid.lock
sudo rm -rf /var/cache/yum
```

#### 강제로 해당 yum/dnf 관련 프로세스 죽이기
```less
ps aux | grep yum

sudo kill -9 19322 19597 20400
```

#### RPM 데이터베이스가 어떤 이유로 손상되거나 꼬였을 때 이를 복구하기 위해 사용

```less
sudo rpm --rebuilddb

yum 또는 rpm 명령이 정상 동작하지 않을 때

패키지 설치/삭제 관련 오류가 발생할 때

yum이 멈추거나 꼬이는 문제를 해결할 때
```

#### 종료 후 다시 진행
```less
먼저 rpm 잠금 상태 초기화
sudo rm -f /var/lib/rpm/__db*
sudo rpm --rebuilddb
```

#### 1단계: 맥에서 필요한 rpm 파일 다운로드
```less
cd /Users/jongwon/test

curl -L -o elrepo-release-7.el7.elrepo.noarch.rpm https://www.elrepo.org/elrepo-release-7.el7.elrepo.noarch.rpm

curl -L -o kmod-wireguard.rpm https://elrepo.org/linux/kernel/el7/x86_64/RPMS/kmod-wireguard-1.0.20210831.el7.elrepo.x86_64.rpm

curl -L -o wireguard-tools.rpm https://elrepo.org/linux/kernel/el7/x86_64/RPMS/wireguard-tools-1.0.20210606.el7.elrepo.x86_64.rpm
```

#### 2단계: 맥에서 서버로 파일 복사 (scp)
```less
scp -P 2222 /Users/jongwon/test/elrepo-release-7.el7.elrepo.noarch.rpm root@smart.apple-box.kr:/root/
scp -P 2222 /Users/jongwon/test/kmod-wireguard.rpm root@smart.apple-box.kr:/root/
scp -P 2222 /Users/jongwon/test/wireguard-tools.rpm root@smart.apple-box.kr:/root/
```

#### 3단계: 서버에서 rpm 파일 설치
```less
sudo rpm -ivh /root/elrepo-release-7.el7.elrepo.noarch.rpm
sudo rpm -ivh /root/kmod-wireguard.rpm
sudo rpm -ivh /root/wireguard-tools.rpm
```

#### 4단계: WireGuard 모듈 로드
```less
sudo modprobe wireguard

modinfo wireguard
```















