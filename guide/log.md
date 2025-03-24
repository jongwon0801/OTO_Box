#### log 조회
```
cd /var/log/

# gz 파일 전부 삭제
sudo rm /var/log/*.gz

# log 파일 전부 삭제
sudo rm /var/log/*.log

rm -rf는 디렉토리 포함 모든 파일을 삭제할 때 사용
```

#### logrotate 설정
```
nano /etc/logrotate.conf

# 버전확인
logrotate --version

nano /etc/logrotate.conf

weekly          # 로그를 매주 회전
rotate 4        # 4주치 로그를 보관
create          # 회전 후 새 로그 파일 생성
```
