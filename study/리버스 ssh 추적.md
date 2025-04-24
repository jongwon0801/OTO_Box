✅ 1. curl 명령

```less
curl -v -X GET \
  --header "Host: applebox-11040.apple-box.kr" \
  "http://smart.apple-box.kr/v1/AutosshStart/11040/22"
```
이건 외부(사실은 내부 스크립트)에서 서버 (smart.apple-box.kr)로 HTTP 요청을 보낸 것

| 구성 요소                                              | 실제 의미                           | 작동 방식                                                           |
|-------------------------------------------------------|------------------------------------|--------------------------------------------------------------------|
| `http://smart.apple-box.kr/v1/AutosshStart/$1/22`     | ✅ 실제 요청을 보내는 서버 주소         | `curl`이 이 URL로 HTTP 요청을 보냄                                     |
| `--header "Host: applebox-$1.apple-box.kr"`           | ❗ HTTP 헤더 중 하나                  | 서버는 이 `Host` 값을 보고 가상호스트 기반 라우팅에 사용함               |


✅ 2. 서버가 Host 헤더를 보고 판단
```less
서버가 Host 헤더를 보고 판단
nginx나 리버스 프록시가 "Host: applebox-11040.apple-box.kr"을 보고

이건 11040 포트로 리버스 터널된 라즈베리파이로 보내야겠구나!

→ 내부적으로 http://127.0.0.1:11040/v1/AutosshStart/11040/22로 프록시 패스
 (applebox-11040.apple-box.kr → 127.0.0.1:11040 으로 내부 포워딩)
```

#### 서버 nginx

```less
server {
    listen 80;
    server_name applebox-11040.apple-box.kr;

    location / {
        proxy_pass http://127.0.0.1:11040;
    }
}
```
✅ 3. 라즈베리파이가 해당 요청 받음

라즈베리파이에서는 마치 누군가가 자기한테 직접 HTTP 요청을 보낸 것처럼 느껴짐

🔁 라즈베리파이의 웹 서버나 API 서버가
"GET /v1/AutosshStart/11040/22" 라는 요청을 받음




```less
1. 클라이언트(curl)는 smart.apple-box.kr로 요청 보냄

2. nginx는 Host 헤더를 보고 applebox-11040.apple-box.kr으로 라우팅함

3. 내부적으로는 127.0.0.1:11040으로 요청 전달됨 → 이건 라즈베리파이 리버스 터널
```

✅ 요약
```less
URL은 요청을 보낼 대상 서버 주소 (외부)
URL : http://smart.apple-box.kr/...

Host는 서버에서 어떤 내부 리버스 터널 포트로 연결할지 결정하는 기준 (내부)
Host 헤더 : applebox-11040.apple-box.kr
```

- curl은 무조건 URL로 요청을 보냄
- 하지만 서버는 Host 헤더를 보고 내부에서 어디로 라우팅할지 판단함


💡 왜 다르게 쓰냐?

📌 이유: 가상 호스팅 / 리버스 프록시 구조 때문
서버에서는 한 IP에 여러 개의 가상 호스트(domain) 를 붙일 수 있음
(이건 nginx, Apache, Caddy, 모두 지원하는 표준적인 구조)


✅ 결론

smart.apple-box.kr → 요청이 도달할 서버

Host: applebox-11040.apple-box.kr → 요청을 누구한테 넘길지 결정하는 단서

실제 요청은 터널을 통해 라즈베리파이로 전달

```less
[ 외부 curl 요청 ]
         ↓
 smart.apple-box.kr (nginx 프록시)
         ↓
 nginx가 Host 헤더 보고
 → proxy_pass http://127.0.0.1:11040
         ↓
 라즈베리파이 (리버스 SSH 포트포워딩)
         ↓
 [ 라즈베리파이의 웹서버 ]
 → "GET /v1/AutosshStart/11040/22"
```


v1은 흔히 쓰는 API 버전 명시 방식
v1은 "버전 1" 이라는 뜻이고, URL 경로 일부로 사용되는 네이밍 규칙


📦 보통 API 설계에서는
```less
/v1/... ← 첫 번째 릴리스

/v2/... ← 기능 변경 또는 개선

/v3/... ← 대규모 리팩터링 후

이렇게 버전별 경로를 따로 유지해서,
옛날 클라이언트가 망가지지 않도록 API를 관리
```





