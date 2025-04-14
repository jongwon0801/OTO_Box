####  /etc/nginx/sites-available/default  (라즈베리파이)

```less
server {
    listen 80 default_server;
    listen [::]:80 default_server;

    root /var/www/html;
    index index.html index.htm index.nginx-debian.html;
    server_name _;

    location /manage {
        root /home/pi/Workspace/newapp/collected_statics;
    }
    location /api {
        root /home/pi/Workspace/newapp/collected_statics;
    }
    location / {
        proxy_pass_request_headers on;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:8000/;
        proxy_redirect off;
    }
    location /cams {
        proxy_pass_request_headers on;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:8765/cams;
        proxy_redirect off;
    }
    location /live {
        proxy_pass_request_headers on;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:8081/live;
        proxy_redirect off;
    }
}

server {
    listen 443;
    charset utf-8;
    access_log /etc/nginx/log/access.log;
    error_log /etc/nginx/log/error.log;
    ssl on;
    ssl_certificate /etc/nginx/ssl/wikibox01-ssl.crt;
    ssl_certificate_key /etc/nginx/ssl/wikibox01-ssl.key;

    location /manage {
        root /home/pi/Workspace/newapp/collected_statics;
    }
    location /api {
        root /home/pi/Workspace/newapp/collected_statics;
    }
    location / {
        proxy_pass_request_headers on;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:8000/;
        proxy_redirect off;
    }
    location /cams {
        proxy_pass_request_headers on;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:8765/cams;
        proxy_redirect off;
    }
    location /live {
        proxy_pass_request_headers on;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Host $http_host;
        proxy_set_header X-NginX-Proxy true;
        proxy_pass http://127.0.0.1:8081/live;
        proxy_redirect off;
    }
}
```
