```less
# 원격접속
#ssh -p 2222 root@smart.apple-box.kr

#pw : tmshdnxmfl (스노우트리)

#netstat -tulnp | grep ssh


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


🔍 프록시와 관련된 흐름 설명

```less
# http 요청
curl -v -X GET --header "Host: applebox-$1.apple-box.kr"  "http://smart.apple-box.kr/v1/AutosshStart/$1/22"
```

#### 1. curl 명령
```less
여기서 curl은 단순한 HTTP 요청을 보내는 것입니다.

Host 헤더는 nginx가 해당 요청을 처리할 때 어떤 호스트 이름을 사용할지 명시하는 부분입니다. 이때 $1 값이 사용됩니다.
```

#### 2. nginx에서 프록시 처리
```less
서버에 있는 nginx가 요청을 받으면, 해당 Host 헤더를 보고 요청을 적절한 내부 서비스로 프록시합니다.

예를 들어, 요청이 applebox-$1.apple-box.kr라는 호스트로 오면,
nginx는 그 요청을 127.0.0.1:11010 (혹은 다른 지정된 포트)로 전달할 수 있습니다.
```

#### 3. nginx는 HTTP 요청을 전달할 뿐
```less
nginx는 HTTP 요청을 프록시하는 역할만 합니다.

이 과정에서 curl 요청을 받는 쪽에서는 사용자 계정이나 SSH 접속과 같은 부분을 신경 쓸 필요가 없습니다. 단순히 HTTP 트래픽만 전달됩니다.
```

#### 4. 라즈베리파이에서 리버스 터널:
```less
라즈베리파이가 reverse SSH 터널을 통해 서버로 포트를 열어두면, nginx가 그 터널로 HTTP 요청을 전달할 수 있게 됩니다.

예를 들어, 요청이 nginx를 통해 들어오면, nginx는 그 요청을 127.0.0.1:11010으로 전달하고,

해당 포트로 트래픽을 라즈베리파이로 전달하는 방식입니다.
```

✅ 결론

```less
curl 명령은 HTTP 요청을 보내는 도구입니다.

이 요청은 사용자 계정 개념이 필요 없다는 점에서, nginx로 전달된 HTTP 요청도 마찬가지로 사용자 계정이나 SSH 로그인과는 관계없습니다.

nginx는 HTTP 요청을 프록시하는 역할만 하며, 사용자 계정과는 관련이 없습니다.
```













