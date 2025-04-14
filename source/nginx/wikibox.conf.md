#### /etc/nginx/conf.d/wikibox.conf (서버)

```less
server {
        listen   80;

        server_name  www.wikibox.kr wikibox.kr;
        location / {
             rewrite ^(.*)$ http://wisemonster.kr redirect;
        }
}
```

