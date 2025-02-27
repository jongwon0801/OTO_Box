# raspberry pi ip 알아 내는 법 3가지

### 1. 라우터의 관리 페이지에서 라즈베리 파이의 할당된 IP 주소를 확인
```bash
wikibox 192.168.0.1
wikibox  /  wiki0800**

wikibox_lab 192.168.1.1
wikibox  /  tmshdnxmfl
```
<img width="637" alt="image" src="https://github.com/user-attachments/assets/927521bb-edb2-4234-841b-d2c09a621737" />

### 2. 라즈베리 파이가 네트워크에 연결된 경우, 다른 장치에서 라즈베리 파이를 raspberrypi.local로 핑 테스트를 하면 IP를 알 수 있습니다.
```bash
ping raspberrypi.local

```
### 3. 직접 장치에 모니터 연결해서 터미널 열고 ifconfig 명령어
