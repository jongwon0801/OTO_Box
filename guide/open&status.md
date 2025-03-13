### 열기 닫기

```python
# applelocker 이동
cd Workspace/newapp/applelocker
```

#### 열기 (닫기는 자동으로 닫혀서 없음)
```python
# 0인자 : 명령, 1인자 : jumper, 2인자 : serial
python ctrl.py open 1 1
-> 1 컨트롤러의 1번 문을 열어라

elif sys.argv[1] =='open' :
            if size == 2:
                lockerList = Locker.objects.filter(kind='B').order_by('col', 'row')
                for item in lockerList:

                    ret = LockerService.openDoor(item.jumper, item.serial)
                    if ret:
                        continue
                    else :
                        print("열기 실패 ")
                        continue
                    #time.sleep(1)
            elif size == 3:
                jumper = int(sys.argv[2])
                lockerList = Locker.objects.filter(jumper=jumper)
                for item in lockerList:
                    LockerService.openDoor(item.jumper, item.serial)
                    time.sleep(1)
            elif size == 4:

                jumper = int(sys.argv[2])
                serial = int(sys.argv[3])
                # lockerList = Locker.objects.get(jumper=jumper,serial=serial)
                # for item in lockerList:
                #    LockerService.openDoor(item.jumper, item.serial)
                #    time.sleep(1)
                #LockerService.makeData(jumper,serial)
                LockerService.openDoor(jumper, serial)

```


#### status 확인
```python
# 모든 사물함의 상태를 확인
python ctrl.py status

# 점퍼(jumper) ID가 1인 모든 락커의 상태를 체크
python ctrl.py status 1

elif sys.argv[1] =='status' :

            if size == 2:
                for j in Locker.objects.raw('SELECT distinct jumper jumper , jumper as id FROM applebox_locker
                                                                       where jumper is not null and jumper>0'):
                    p = LockerService.statusBoard(j.jumper)
            elif size == 3:
                jumper = int(sys.argv[2])
                p = LockerService.statusBoard(jumper) # 상태
```

- sys.argv[2] = '1' → jumper = 1
- LockerService.statusBoard(1) 실행
- 즉, LockerService.statusBoard(1) 함수가 jumper=1인 모든 락커의 상태를 조회합니다.




