#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import serial
import time

def open_door(jumper, serial_num):
    """특정 보드와 시리얼 번호의 도어를 여는 함수"""
    try:
        # 시리얼 포트 열기 (실제 포트 이름으로 변경 필요)
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        
        # 명령어 생성 및 전송
        command = f"OPEN:{jumper}:{serial_num}\n"
        ser.write(command.encode())
        
        # 응답 읽기
        response = ser.readline().decode().strip()
        ser.close()
        
        print(f"도어 {jumper}-{serial_num} 열기 명령 전송 결과: {response}")
        return "OK" in response
    except Exception as e:
        print(f"에러 발생: {e}")
        return False

def check_status(jumper):
    """특정 보드의 상태를 확인하는 함수"""
    try:
        # 시리얼 포트 열기
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
        
        # 상태 확인 명령어 전송
        command = f"STATUS:{jumper}\n"
        ser.write(command.encode())
        
        # 응답 읽기
        response = ser.readline().decode().strip()
        ser.close()
        
        print(f"보드 {jumper} 상태: {response}")
        return response
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python script.py [명령어] [인자...]")
        print("명령어:")
        print("  open [jumper] [serial] - 특정 도어 열기")
        print("  status [jumper] - 보드 상태 확인")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "open" and len(sys.argv) >= 4:
        jumper = int(sys.argv[2])
        serial_num = int(sys.argv[3])
        open_door(jumper, serial_num)
        
    elif command == "status" and len(sys.argv) >= 3:
        jumper = int(sys.argv[2])
        check_status(jumper)
        
    else:
        print("잘못된 명령어 또는 인자입니다.")
