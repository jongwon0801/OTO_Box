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
