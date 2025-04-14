# -*- coding: utf-8 -*-
import threading
from . import rs485

lock = threading.Lock()
def openDoorSimple(jumper, serial):
    # 임시로 만들어서 지워야 합니다 .
    #lock = threading.Lock()
    global  lock
    lock.acquire()
    try:
        rs485.init()
        rp = rs485.openDoorSimple(jumper, serial)
        rs485.close()
        #print(rp)
        # if rp:
        # app.lockerEvent.updateLockerStatus(jumper,serial,'E')

        return rp
    except Exception as e:
        print(e)
    finally:
        rs485.close()
        lock.release()
    return None
def makeData(j,s):
    rs485.makeData(j,s)
def openDoor(jumper, serial, portName='/dev/hunes'):
    # 임시로 만들어서 지워야 합니다 .
    #lock = threading.Lock()
    global lock
    lock.acquire()
    try:
        rs485.init(portName)
        rp = rs485.openDoor(jumper, serial)
        rs485.close()
        #print(rp)
        # if rp:
        # app.lockerEvent.updateLockerStatus(jumper,serial,'E')

        return rp
    except Exception as e:
        print(e)
    finally:
        rs485.close()
        lock.release()
    return None
def testStatus(portName,jumper=1):
    return rs485.testStatus(portName,jumper)
def initDoor(jumper, portName='/dev/hunes'):
    # 임시로 만들어서 지워야 합니다 .
    #lock = threading.Lock()
    global lock
    lock.acquire()
    try:
        rs485.init(portName)
        rp = rs485.initDoor(jumper)
        rs485.close()
        #print(rp)
        # if rp:
        # app.lockerEvent.updateLockerStatus(jumper,serial,'E')

        return rp
    except Exception as e:
        print(e)
    finally:
        rs485.close()
        lock.release()
    return None

def isOn(jumper, serial, portName='/dev/hunes'):
    p = statusBoard(jumper,portName)
    if p:
        return rs485.isOn(p, serial)
    return False


def statusSensors(jumpers, portName='/dev/hunes'):
    global lock
    lock.acquire()
    try:
        rs485.init(portName)

        rp = rs485.statusSensors(jumpers)
        rs485.close()
        return rp
    finally:
        lock.release()

def statusSensor(jumper, portName='/dev/hunes'):
    global lock
    lock.acquire()
    try:
        rs485.init(portName)

        rp = rs485.statusSensor(jumper)
        rs485.close()
        return rp
    finally:
        lock.release()
def statusBoard(jumper, portName='/dev/hunes'):
    global lock
    lock.acquire()
    try:
        rs485.init(portName)

        rp = rs485.statusBoard(jumper)
        rs485.close()
        return rp
    finally:
        lock.release()
def statusBoard1(jumper,id, portName='/dev/hunes'):
    global lock
    #lock = threading.Lock()
    lock.acquire()
    try:
        print('start %d'%id)
        rs485.init(portName)

        rp = rs485.statusBoard(jumper)
        rs485.close()

        return rp
    finally:
        print('end %d' % id)
        lock.release()

