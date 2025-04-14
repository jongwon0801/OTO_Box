#### /etc/nginx/conf.d/applebox-locker.conf (서버)


#### startssh.sh

```less
#echo $1
#echo $2
#cmd1=\'abcd$1\'
#echo $cmd1
curl -v -X GET --header "Host: applebox-$1.apple-box.kr"  "http://smart.apple-box.kr/v1/AutosshStart/$1/22"
sleep 5
ssh -p "$(($1+30000))" pi@localhost
wait
curl -v -X GET --header "Host: applebox-$1.apple-box.kr"  "http://smart.apple-box.kr/v1/AutosshStop"
```

```less
server {

  listen       80;

  server_name   "~^applebox-(?<port>\d{4,5})\.apple-box\.kr$";
underscores_in_headers on;
  location / {
    proxy_pass        http://127.0.0.1:$port;
    proxy_set_header  X-Real-IP  $remote_addr;
    proxy_set_header  Host $host;
        proxy_pass_request_headers on;
  }
#error_log logs/error.log warn;
#error_page 502 504 =200 @50*_json;

#  location @50*_json {
#    default_type application/json;
#    return 502 '{"success":false,"code":"1", "message": "Unknown Error"}';
#  }
}
```
