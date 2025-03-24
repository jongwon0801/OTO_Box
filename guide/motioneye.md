#### motioneye device 확인

```
192.168.0.20 춘의동 세탁소

# video 파일 저장 장소
cd /var/lib/motioneye/Camera1

# 모든 녹화파일 삭제
rm -rf /var/lib/motioneye/Camera1/*

```
<img src="https://github.com/user-attachments/assets/f77c3447-4345-433b-9c78-49cf65e44339" width="400" height="300" />

<img src="https://github.com/user-attachments/assets/1ec2f896-6a39-4e2b-8c02-4e7d581a3338" width="400" height="300" />

<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/11ef1a66-9d22-435f-9291-887e7a0f2bf8" />

#### 영상 삭제 주기 설정

#### Preserve Movies
<img width="400" height="300" alt="image" src="https://github.com/user-attachments/assets/4e6da08f-2298-4699-881a-501c658784ec" />



#### 연결된 영상 장치 확인

```
cd /dev

# USB 장치 확인
lsusb

# 비디오 장치 확인
ls /dev/video*

v4l2-ctl --list-devices

```

#### motioneye 전체설정확인
```
/etc/motioneye

# MotionEye는 각 카메라의 설정을 개별적으로 저장
sudo nano /etc/motioneye/camera-1.conf

# MotionEye 전체 설정
sudo nano /etc/motioneye/motion.conf

# /dev/video5가 진짜 카메라 데이터를 전달받고 있는 가상 장치
ffplay /dev/video5
```



