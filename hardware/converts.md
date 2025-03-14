#### USB to RS485 Converter


📌 가능한 부품 종류
1️⃣ USB to TTL(UART) 변환 모듈

<img src="[image_url](https://github.com/user-attachments/assets/c7aea309-f7f5-4932-ac13-5d85bdf76467)" width="300" height="200"/>




📌 용도: 아두이노, 라즈베리파이, ESP32 같은 마이크로컨트롤러와 PC 연결

📌 주요 칩셋: CP2102, CH340, FT232RL 등

📌 선 색상 예시:
```
빨강 (VCC, 5V 또는 3.3V)
검정 (GND)
흰색 (RX, 데이터 수신)
녹색 (TX, 데이터 전송)
```

2️⃣ USB to RS485 변환기

<img src="[image_url](https://github.com/user-attachments/assets/f1a718bb-2397-4a5d-a872-16f9f0f1abff)" width="300" height="200"/>


📌 용도: 산업용 통신(RS485 방식), 모터 컨트롤러, PLC, 센서 연결

📌 터미널 블록에 연결 가능:
```
A(+) → 흰색
B(-) → 녹색
GND → 검정
VCC(전원) → 빨강 (일부 모델에서는 없을 수도 있음)
```

3️⃣ USB 전원 공급 케이블 (USB to DC 5V or 터미널 블록용)


![image](https://github.com/user-attachments/assets/682e8c3c-5ff6-47ef-85ae-42fecedfa3eb)


📌 용도: 전자기기에 USB 전원(5V) 공급

📌 터미널 연결 예시:
```
빨강 → 5V
검정 → GND
다른 두 개(흰색, 녹색)는 데이터 선이지만 전원용 케이블에서는 안 쓰일 수도 있음
🔍 어떤 부품인지 확인하는 방법
✔ 터미널 블록에 A, B 표기되어 있으면? → USB to RS485 변환기
✔ RX, TX라고 써 있으면? → USB to TTL(UART) 변환기
✔ 전원(5V, GND)만 있으면? → USB 전원 공급 케이블
```


