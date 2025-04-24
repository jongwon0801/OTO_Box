```less
server {
  listen 80;
  server_name "~^applebox-(?<port>\d{4,5})\.apple-box\.kr$";
  underscores_in_headers on;

  location / {
    proxy_pass http://127.0.0.1:$port;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header Host $host;
    proxy_pass_request_headers on;
  }
}
```

```less
1. 서버 이름 패턴 매칭: server_name 지시문은 정규 표현식을 사용하여 applebox-포트번호.apple-box.kr 형식의 호스트명을 매칭
applebox-11040.apple-box.kr 요청이 들어오면, 정규 표현식에서 11040을 추출하여 $port 변수에 저장

2. 프록시 전달: 매칭된 요청은 proxy_pass 지시문을 통해 http://127.0.0.1:$port로 전달
추출된 포트 번호를 사용하여 로컬호스트의 해당 포트로 요청을 프록시

3. 헤더 설정: proxy_set_header 지시문을 통해 클라이언트의 실제 IP 주소와 호스트명을 전달
```

| 변수           | 의미                                | 어디서 오는지                         |
|----------------|-------------------------------------|--------------------------------------|
| `$remote_addr` | 요청 보낸 사람의 IP 주소            | NGINX가 직접 TCP 연결에서 얻음       |
| `$host`        | 요청의 Host 헤더 (도메인)           | 클라이언트가 HTTP 헤더에 넣어 보낸 값 |












