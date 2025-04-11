#### 개념 정리: 11040 vs 41040

① 11040 — 서버에서 listen 중인 웹 포트 (예: HTTP API 포트)
서버가 자체적으로 운영 중인 서비스 포트 (예: Flask API, Nginx 리버스 프록시)

예: http://smart.apple-box.kr/v1/AutosshStart/11040/22 처럼 사용됨

보통 AutosshStart, AutosshStop 같은 API 요청 받을 때 씀

```less
ss -tulnp | grep 11040
tcp    LISTEN     0      128    127.0.0.1:11040     *:*    users:(("sshd",pid=xxxxx))
```

② 41040 — Pi에서 reverse SSH로 터널링한 포트
ssh -R 41040:localhost:22 root@smart.apple-box.kr
👉 이 명령의 의미는:

서버의 41040 포트에 접근하면, Pi의 22번 포트(SSH)로 포워딩하겠다!

즉, 서버 입장에서 보면:

누군가 localhost:41040으로 접속하면

실제로는 라즈베리파이의 SSH 포트로 연결됨


| 포트   | 역할                              | 열려있는 위치     | 용도                                      |
|--------|-----------------------------------|-------------------|-------------------------------------------|
| 11040  | API listen 포트 (ex. AutosshStart 요청용) | 서버              | 웹 요청 처리                              |
| 41040  | reverse SSH 터널 포트             | 서버 (역으로 Pi가 열어줌) | 서버가 Pi에 SSH로 접속할 수 있게 해줌    |


예시 흐름 (자동 연결 과정)

1. 서버에서 startssh.sh 11040 실행 → API 호출됨 (AutosshStart)

2. 라즈베리파이가 명령 받아서 아래 실행:

```less
ssh -p 2222 -R 41040:localhost:22 root@smart.apple-box.kr
```

3. 이제 서버에서 아래 명령으로 Pi에 접속 가능:
```less
ssh -p 41040 pi@localhost
```




