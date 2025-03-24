#### Django 개발 서버는 기본적으로 포트 8000에서 실행

```
# 실행 상태 확인
ps aux | grep manage.py

pi         622  0.0  1.8  75720 34072 ?        Ssl   3월22   2:32 /home/pi/.virtualenvs/o2obox/bin/python
 /home/pi/Workspace/newapp/manage.py runserver 0.0.0.0:8000 --noreload
pi       27677  0.0  0.0   6248   576 pts/0    S+   12:55   0:00 grep --color=auto manage.py

# 프로세스 종료
kill 622

# 서버 재시작
python3 manage.py runserver 0.0.0.0:8000

```
