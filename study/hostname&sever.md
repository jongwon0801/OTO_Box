
#### 1. hostname 명령어

```   
hostname 명령어는 별도의 import 없이 실행할 수 있으며, 현재 시스템의 호스트명을 반환합니다.

이는 /etc/hostname 파일이나 네트워크 설정에서 가져옵니다.
```

<br>

```
$ hostname
raspberrypi
```

<br>

#### 2. server (호스트명 해석)
```
server는 특정한 명령어가 아니라, /etc/hosts 또는 DNS 설정에서 정의된 호스트명을 의미합니다.
```

<br>

예를 들어, /etc/hosts 파일에 다음과 같이 정의되어 있다면

```
10.100.80.100 server
```

#### 이제 터미널에서 ping server 같은 명령을 실행하면, server는 자동으로 10.100.80.100으로 변환됩니다.
```
$ ping server
PING server (10.100.80.100) 56(84) bytes of data.
```

<br>

#### 즉, 별도로 import할 필요 없이 시스템이 알아서 /etc/hosts나 DNS에서 해당 호스트명을 찾아 IP로 변환합니다.

<br>

#### 결론
```
✅ hostname 명령어는 시스템의 호스트명을 반환하는 기본 명령어이며, 별도의 import 없이 사용 가능

✅ server 같은 호스트명은 /etc/hosts 또는 DNS 설정에서 자동으로 IP로 변환됨

✅ 별도 import 없이 사용할 수 있지만, 특정 네트워크 환경에서 동작 방식이 다를 수 있음
```

<br>

#### 1. /etc/hostname
```
역할: 이 파일에는 **현재 시스템의 호스트명(컴퓨터 이름)**이 저장되어 있음.

내용: 단 한 줄로, 시스템의 호스트명만 포함.
```

#### 참고 위치
```
hostname 명령어 실행 시 이 값을 참조함.

부팅 시 이 값을 읽어서 시스템의 호스트명을 설정함.
```

<br>

```
$ cat /etc/hostname
raspberrypi

$ hostname
raspberrypi
```

<br>

#### 2. /etc/hosts

```
역할: 특정 호스트명을 IP 주소에 매핑하는 로컬 네임 해석 파일.

내용: 여러 줄을 포함할 수 있으며, 특정 호스트명에 대한 IP 주소를 지정할 수 있음.
```

#### 참고 위치

```
도메인 이름을 IP 주소로 변환할 때, DNS보다 먼저 /etc/hosts를 조회함.

ping server 같은 명령을 실행할 때, /etc/hosts에 해당 매핑이 있으면 해당 IP로 변환됨.
```

<br>

#### 예시 (/etc/hosts 내용)

```
127.0.0.1       localhost
::1             localhost ip6-localhost ip6-loopback
10.100.80.100   server
125.209.200.159 vpnserver
```
<br>

#### 명령어 확인

```
$ ping server
PING server (10.100.80.100) 56(84) bytes of data.
```

<br>

차이점 요약

| 구분         | `/etc/hostname`            | `/etc/hosts`                      |
|-------------|--------------------------|---------------------------------|
| **역할**     | 시스템의 호스트명 저장        | 호스트명 ↔ IP 주소 매핑          |
| **파일 내용** | 단 한 줄, 호스트명만 포함    | 여러 개의 IP-호스트명 매핑 가능   |
| **예제**     | `raspberrypi`            | `10.100.80.100 server`          |
| **관련 명령어** | `hostname`              | `ping`, `ssh`, `scp` 등 네트워크 관련 명령 |
| **적용 시점** | 부팅 시 반영됨             | 즉시 반영됨                      |

<br>

#### 결론
```
/etc/hostname: 시스템의 고유 이름을 저장하는 파일.

/etc/hosts: 특정 호스트명을 IP로 변환하는 로컬 네임 해석 파일.

두 파일 모두 시스템에서 중요한 역할을 하며, hostname은 시스템의 이름을 지정하고, hosts는 네트워크에서 IP-호스트명을 매핑하는 용도로 사용됩니다.
```
