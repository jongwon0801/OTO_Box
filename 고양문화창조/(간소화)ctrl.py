#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import serial
import time

def open_door(jumper, serial_num):
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
        time.sleep(0.5)
        
        command = f"OPEN:{jumper}:{serial_num}\n"
        print(f"명령어 전송: {command.strip()}")
        ser.write(command.encode())
        
        responses = []
        for _ in range(5):
            response = ser.readline().decode().strip()
            if response:
                responses.append(response)
            else:
                break
        
        ser.close()
        
        if responses:
            print(f"도어 {jumper}-{serial_num} 열기 명령 전송 결과: {', '.join(responses)}")
            return "OK" in ' '.join(responses)
        else:
            print(f"도어 {jumper}-{serial_num} 열기 명령에 대한 응답 없음")
            return False
    except Exception as e:
        print(f"에러 발생: {e}")
        return False

def check_status(jumper, serial_num=None):
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
        time.sleep(0.5)
        
        if serial_num is None:
            command = f"STATUS:{jumper}\n"
        else:
            command = f"STATUS:{jumper}:{serial_num}\n"
        
        print(f"명령어 전송: {command.strip()}")
        ser.write(command.encode())
        
        responses = []
        for _ in range(5):
            response = ser.readline().decode().strip()
            if response:
                responses.append(response)
            else:
                break
        
        ser.close()
        
        if responses:
            if serial_num is None:
                print(f"보드 {jumper} 상태: {', '.join(responses)}")
            else:
                print(f"도어 {jumper}-{serial_num} 상태: {', '.join(responses)}")
            return responses
        else:
            if serial_num is None:
                print(f"보드 {jumper} 상태 확인에 대한 응답 없음")
            else:
                print(f"도어 {jumper}-{serial_num} 상태 확인에 대한 응답 없음")
            return None
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

def init_door(jumper):
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
        time.sleep(0.5)
        
        command = f"INIT:{jumper}\n"
        print(f"명령어 전송: {command.strip()}")
        ser.write(command.encode())
        
        responses = []
        for _ in range(5):
            response = ser.readline().decode().strip()
            if response:
                responses.append(response)
            else:
                break
        
        ser.close()
        
        if responses:
            print(f"보드 {jumper} 초기화 명령 전송 결과: {', '.join(responses)}")
            return "OK" in ' '.join(responses)
        else:
            print(f"보드 {jumper} 초기화 명령에 대한 응답 없음")
            return False
    except Exception as e:
        print(f"에러 발생: {e}")
        return False

def check_sensor(jumper):
    try:
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=3)
        time.sleep(0.5)
        
        command = f"SENSOR:{jumper}\n"
        print(f"명령어 전송: {command.strip()}")
        ser.write(command.encode())
        
        responses = []
        for _ in range(5):
            response = ser.readline().decode().strip()
            if response:
                responses.append(response)
            else:
                break
        
        ser.close()
        
        if responses:
            print(f"보드 {jumper} 센서 상태: {', '.join(responses)}")
            return responses
        else:
            print(f"보드 {jumper} 센서 상태 확인에 대한 응답 없음")
            return None
    except Exception as e:
        print(f"에러 발생: {e}")
        return None

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("사용법: python ctrl.py [명령어] [인자...]")
        print("명령어:")
        print("  open [jumper] [serial] - 특정 도어 열기")
        print("  status [jumper] - 보드 전체 상태 확인")
        print("  status [jumper] [serial] - 특정 도어 상태 확인")
        print("  init [jumper] - 특정 보드 초기화")
        print("  sensor [jumper] - 특정 보드의 센서 상태 확인")
        sys.exit(1)
        
    command = sys.argv[1]
    
    if command == "open" and len(sys.argv) >= 4:
        jumper = int(sys.argv[2])
        serial_num = int(sys.argv[3])
        open_door(jumper, serial_num)
        
    elif command == "status":
        if len(sys.argv) >= 3:
            jumper = int(sys.argv[2])
            if len(sys.argv) >= 4:
                serial_num = int(sys.argv[3])
                check_status(jumper, serial_num)
            else:
                check_status(jumper)
        else:
            print("점퍼 번호를 지정해주세요.")
            
    elif command == "init" and len(sys.argv) >= 3:
        jumper = int(sys.argv[2])
        init_door(jumper)
        
    elif command == "sensor" and len(sys.argv) >= 3:
        jumper = int(sys.argv[2])
        check_sensor(jumper)
        
    else:
        print("잘못된 명령어 또는 인자입니다.")
