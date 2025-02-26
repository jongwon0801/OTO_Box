# /root/kdone.py

#!/usr/bin/python3
# -*- coding: UTF-8 -*-
import serial
import sys
import time
from threading import Thread
import mysql.connector
from dateutil import tz
import datetime
#[247, 50, 0, 
# 122, =command
# 25,  = length
# 50, 
# 0, 
# 0, 0, 0, 0, 
# 0, 0, 0, 0, 
# 0, 0, 
# 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, ==field data 13개 
# 50, 32]
class KdoneThread(Thread):

    def __init__(self):
        Thread.__init__(self)
        self.ser = serial.Serial()
        #self.ser.port='/dev/smartro'
        self.ser.port = '/dev/ttyUSB0'
        self.ser.baudrate=9600
        self.ser.parity=serial.PARITY_NONE
        self.ser.stopbits=serial.STOPBITS_ONE
        self.ser.bytesize=8
        self.ser.timeout=3
    def run(self):
        conti = True
        while conti:
            try:
                if self.ser.isOpen()==False:
                    self.doConnect()
                rb = self.readPacket()
                if rb:
                    self.parsePacket(rb)
            except Exception as e:
                print(e)
                time.sleep(10)

    def parsePacket(self,d):
        header = d['header']
        data = d['data']
        if header[3]==0x79: # Equipment_info_query
            fdata =data[12:] # field data
            dong = int.from_bytes(fdata[0:2], "big")      
            ho = int.from_bytes(fdata[2:4], "big")   

            if dong ==0 and ho==0 :
                #self.selectNewList(3)
                boxList=self.selectNewList(3)
                rp = self.makePacket('0','0',boxList)
                self.ser.send(rp)
                self.update(boxList)
            else:
                boxList= self.select(str(dong),str(ho))
                rp = self.makePacket(str(dong),str(ho),boxList)
                self.ser.send(rp)
                self.update(boxList)
        else:
            rp = self.makePacket('0','0',self.selectNewList(3))
            self.ser.send(rp)
    def makePacket(self,dong, ho, boxList):

        

        data_id= [0x32,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00]
        data_info=[0x00,0x00] # 004 byte
        data_fdata=[]

        

        if len(boxList)==0:
            data_fdata=data_fdata+list(int(dong).to_bytes(2, byteorder='big')) # 2  
            data_fdata=data_fdata+list(int(ho).to_bytes(2, byteorder='big')) #2
            data_fdata=data_fdata+[0x00] #갯수 1 
            data_fdata=data_fdata+[0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00,0x00] #
        else:
            data_fdata=data_fdata+list(int(boxList[0].get('toDong')).to_bytes(2, byteorder='big'))
            data_fdata=data_fdata+list(int(boxList[0].get('toHo')).to_bytes(2, byteorder='big'))
            data_fdata=data_fdata+[0xff&len(boxList)] #갯수 

            
            for item in boxList:

                ddata = []
                d1 = datetime.datetime.strptime(item["saveDate"], "%Y-%m-%dT%H:%M:%S.%fZ")

                d1 = d1.replace(tzinfo=tz.gettz('UTC'))

                saveDate = d1.astimezone(tz.gettz('Asia/Seoul'))
                ddata=ddata+list(saveDate.year.to_bytes(2, byteorder='big'))
                ddata=ddata+list(saveDate.month.to_bytes(1, byteorder='big'))
                ddata=ddata+list(saveDate.day.to_bytes(1, byteorder='big'))
                ddata=ddata+list(saveDate.hour.to_bytes(1, byteorder='big'))
                ddata=ddata+list(saveDate.minute.to_bytes(1, byteorder='big'))
                ddata=ddata+list(saveDate.second.to_bytes(1, byteorder='big'))
                ddata=ddata+list((saveDate.weekday()+1).to_bytes(1, byteorder='big'))

                ddata=ddata+list(int(item.get('label')[1:]).to_bytes(2, byteorder='big'))
                if item.get('status')=='A':
                    ddata=ddata+[0x01]
                else:
                    ddata=ddata+[0x00]

                data_fdata=data_fdata+ddata
        stx=0xF7
        device_id=0x32
        sub_id=0x00
        command=0x7A
        data_length=len(data_id)+len(data_info)+len(data_fdata)

        header = [stx, device_id, sub_id,command,data_length] 
        
        data  = data_id+data_info+data_fdata
        checksum = [self.getChecksum(data)]
        addsum = [self.getAddsum(header+data+checksum)]

        return header + data+ checksum+addsum
    def update(self,boxList): # 삼성

        #print(sendData)
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                database='yellowbox',
                user="yellowbox",
                passwd="dpfshdnqkrtm",connect_timeout=2
            )
            mycursor = mydb.cursor()
            for item in boxList:
                dong=item.get('toDong')
                ho=item.get('toHo')
                mycursor.execute("update locker set ustate=0 where dong='"+dong+"',ho='"+ho+"'")
            mydb.commit()
            mycursor.close()
            mydb.close()
        except Exception as e:
            print(e)
            return False

        return True
    def select(self,dong,ho):
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                database='yellowbox',
                user="yellowbox",
                passwd="dpfshdnqkrtm",connect_timeout=2
            )
            mycursor = mydb.cursor(dictionary=True)

            mycursor.execute("select * from locker where toDong='"+dong+"' and toHo='"+ho+"'")
            myresult1 = mycursor.fetchall()
        
            #mydb.commit()
            mycursor.close()
            mydb.close()
            return myresult1
        except Exception as e:
            print(e)
            return None

        return None    
    def selectNewList(self,cnt=3): # 삼성
        try:
            mydb = mysql.connector.connect(
                host="localhost",
                database='yellowbox',
                user="yellowbox",
                passwd="dpfshdnqkrtm",connect_timeout=2
            )
            mycursor = mydb.cursor(dictionary=True)

            mycursor.execute("select * from locker where ustate=1 and status='A' limit 1")
            myresult1 = mycursor.fetchall()
            if len(myresult1)>0:

                mycursor.execute("select * from locker where toDong='"+myresult1[0].get('toDong')+"' and toHo='"+myresult1[0].get('toHo')+"' and ustate=1 limit 3")
                myresult1 = mycursor.fetchall()
            
        
            #mydb.commit()
            mycursor.close()
            mydb.close()
            return myresult1

        except Exception as e:
            print(e)
            return None

        
    
    def doConnect(self):
        self.ser.open()
        self.ser.flushInput()
        self.ser.flushOutput()

    def readPacket(self):
        header = self.ser.read(5)
        print('read',header)
        len = header[-1]
        data  = self.ser.read(len)
        print('read',data)
        checksum = self.ser.read(1)
        addsum = self.ser.read(1)
        print('read checksum',checksum)
        print('read addsum',addsum)
        rchecksum = self.getChecksum(header+data)
        if rchecksum==checksum[0]:
            raddsum = self.getAddsum(header+data+checksum)
            if raddsum==addsum[0]:
                return {'header':header,'data':data}
        return None
    def getChecksum(self,data):
        cs=0x00
        for d in data:
            cs = cs ^ d
        return cs
    def getAddsum(self,data):
        as1=0x00
        for d in data:
            as1 = as1 +d
        return 0xFF & as1

    def close(ser):
        ser.close()



if __name__ == '__main__':

    thread=KdoneThread()
    thread.start()
    #r = thread.makePacket('0','0',thread.select(3))
    #print(r)
