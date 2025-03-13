### 네트워크 연결 x 경우 라즈베리파이 접속 방법 (AP모드 활용)

```
# AP 모드는 Access Point(액세스 포인트) 모드의 줄임말

# 무선 공유기(Wi-Fi 핫스팟)처럼 동작하는 모드
```

#### 1. 라즈베리파이 wifi 로 접속

<img width="452" alt="image" src="https://github.com/user-attachments/assets/8e75fa1b-87da-4747-98ab-9a01f3d9c2bd" />


#### 2. IP 주소, 라우터 주소 확인

<img width="257" alt="image" src="https://github.com/user-attachments/assets/c4a5f3bd-7e99-40b2-bbea-8d07e778f1ad" />

```
IP 주소: 맥북이 라우터(공유기)에서 할당받은 내부 네트워크 주소

라우터(게이트웨이) 주소: 맥북이 인터넷으로 나갈 때 거치는 공유기 주소

# 보통 넷마스크 /24 일경우 255.255.255.0 -> 0번은 네트워크주소, 1은 게이트웨이, 255 브로드캐스트
```

#### 3. 라우터 ip 주소로 ssh 접속

```
ssh pi@172.24.1.1
```
<img width="452" alt="image" src="https://github.com/user-attachments/assets/4e932681-9c95-4ca5-9ae1-afbe8fb6d646" />
