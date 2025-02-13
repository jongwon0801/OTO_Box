#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8

import os
import sys
import django
import json
import requests
import codecs
import time
import threading
import datetime
#from applebox.models import Locker,LockerForm,Log,LogForm,Rfid,SaveLog,TakeLog
sys.path.append("../") #path to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'appleapp.settings'
#django.setup()
from django.forms.models import model_to_dict
from annoying.functions import get_object_or_None
import jwt
'''
락상태 

상위 바이트가  0 이면 닫혀있음
            1 이면 열려있음

센터

상위바이트가  0이면 감지  
          1이면 고장 감지 안됨 
'''
def run():

    #apikey='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I'
    #rt = jwt.decode(apikey, 'ilovescotchyscotch', algorithms=['HS256'])
    #print(rt)
    yid = int(os.uname()[1].split('-')[1])
    size = len(sys.argv)
    if size==1 :
        for j in Locker.objects.raw('SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null and jumper > 0'):
            p = LockerService.statusBoard(j.jumper)

    else :
        if sys.argv[1] == 'simple':
            jumper = int(sys.argv[2])
            serial = int(sys.argv[3])
            # lockerList = Locker.objects.get(jumper=jumper,serial=serial)
            # for item in lockerList:
            #    LockerService.openDoor(item.jumper, item.serial)
            #    time.sleep(1)
            LockerService.openDoorSimple(jumper, serial) # 열기
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
        elif sys.argv[1] =='status' :

            if size == 2:
                for j in Locker.objects.raw('SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null and jumper>0'):
                    p = LockerService.statusBoard(j.jumper)
            elif size == 3:
                jumper = int(sys.argv[2])
                p = LockerService.statusBoard(jumper) # 상태

            elif size == 4:
                jumper = int(sys.argv[2])
                serial = int(sys.argv[3])
                p = LockerService.isOn(jumper,serial)
                print(p)
        elif sys.argv[1] =='sensor' :

            jumper = int(sys.argv[2])
            p = LockerService.statusSensor(jumper) # 상태
            print(p)
        elif sys.argv[1] =='sensors' :
            ds =[]
            cv = Property.objects.filter(name='controller_version').first()
            if cv and cv.value == '2':
                for j in Locker.objects.raw(
                        'SELECT distinct jumper, jumper as id FROM applebox_locker where jumper is not null and jumper>0'):
                    ds.append(j.jumper)
                p = LockerService.statusSensors(ds) # 상태
                print(p)
            else:
                print('지원되지 않는 버젼입니다')



        elif sys.argv[1] == 'init':
            if size == 3:
                jumper = int(sys.argv[2])
                LockerService.initDoor(jumper); # 초기화
        else :
            print('invalid command')
    '''
    try:
        #lockerInfo = Locker.objects.get(yid=17, jumper=2,serial=1)
        #LockerService.openDoor(lockerInfo.jumper, lockerInfo.serial)
        LockerService.openDoor(1, 1)
    except Exception as e:
        print(e)
    '''
class Test(threading.Thread):
    def __init__(self, id):
        threading.Thread.__init__(self)
        self.id = id

    def run(self):
        while True:
            LockerService.statusBoard1(1, self.id)

def iso_format(dt):
    try:
        utc = dt + dt.utcoffset()
    except TypeError as e:
        utc = dt
    isostring = datetime.datetime.strftime(utc, '%Y-%m-%dT%H:%M:%S.{0}Z')
    return isostring.format(int(round(utc.microsecond/1000.0)))
if __name__ == '__main__':
    django.setup()
    from applebox.models import Applebox, Locker,TakeLog,Property
    from applelocker import LockerService
    '''
    lockerList = Locker.objects.filter(kind='B').order_by('col','row')
    for item in lockerList:
        print(item.col,item.row,item.jumper,item.serial)
        #LockerService.openDoor(item.jumper, item.serial)
        #time.sleep(1)
    '''


    #saveDate = iso_format(datetime.datetime.utcnow())
    #print(saveDate)
    run()
    '''
    Test(1).start()
    Test(2).start()
    Test(3).start()
    Test(4).start()
    '''
