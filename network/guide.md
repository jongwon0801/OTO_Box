#### 보관함 관리 가이드


#### 1. 전체 파일 시스템의 사용량을 확인

```
df -h
```

#### 2. MotionEye 명령어

```
# MotionEye 서비스를 중지
sudo systemctl stop motioneye

# 재부팅 시 자동 시작 막기
sudo systemctl disable motioneye

# 다시 시작
sudo systemctl start motioneye

```

#### 3. 라즈베리파이 용량 부족 시 파일 삭제 명령어

```
sudo rm -rf /var/log/*.log

로그 파일 크기 줄이기 (파일은 유지, 내용만 삭제)

sudo truncate -s 0 /var/log/syslog

```




