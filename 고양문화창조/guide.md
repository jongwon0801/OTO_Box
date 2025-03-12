
#### 접속

#### (캡쳐 1) 보관함 서버 관리자 로그인 -> '고양' 단어로 검색 >> 고양문화창조허브 1, 2(11048,11047) 대상 선택 -> 현황 

#### (캡처 2) 11048 접속 ~ date 까지 

- 원격 접속 smart.apple-box.kr (root로)

```bash
# 원격접속
ssh -p 2222 root@smart.apple-box.kr

pw : tmshdnxmfl (스노우트리)
```

```bash
# 11048 접속
./startssh.sh 11048

# 패스워드 tmshdnxmfl 입력

date
```

```bash
# 11047 접속
./startssh.sh 11047

# 패스워드 tmshdnxmfl 입력

date
```
#### (캡처 3)
```bash
# 디스크 사용량 조회
df -h
```

#### (캡처 4)
```bash
# applelocker 이동
cd Workspace/newapp/applelocker

# 모든 사물함의 상태를 확인
python ctrl.py status
```

#### (캡처 5)
```bash
# 실시간으로 CPU, 메모리, 프로세스 사용량을 시각적으로 확인
htop
```





