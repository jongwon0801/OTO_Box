#### log 조회
```
cd /var/log/

# gz 파일 전부 삭제
sudo rm /var/log/*.gz
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
