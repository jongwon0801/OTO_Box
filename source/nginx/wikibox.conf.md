#### /etc/nginx/conf.d/wikibox.conf

```less
server {
        listen   80;

        server_name  www.wikibox.kr wikibox.kr;
        location / {
             rewrite ^(.*)$ http://wisemonster.kr redirect;
        }
}
```

