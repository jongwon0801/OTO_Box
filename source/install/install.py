#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
import sqlite3
import sys
#import mysql.connector
#import MySQLdb
import json,codecs
import requests
import os
import requests
import pprint
yid = int(os.uname()[1].split('-')[1])
#yid=10000

import argparse

parser = argparse.ArgumentParser(description='박스 생성 ')
parser.add_argument('buyerSq', nargs='?', type=int, help='판매자 아이디')
parser.add_argument('-b', '--boxes',required=True,nargs='+', choices=['a', 'b', 'c'], help='박스 구조')
parser.add_argument('-n','--name', required=True, help='이름')
parser.add_argument('-l','--location', help='gps 위치')
parser.add_argument('-a','--addr', help='주소')
parser.add_argument('-s', '--skips',required=True,nargs='+', type=json.loads, help='건너뛰기')
args = parser.parse_args()

o2obox = {"addr": None,
        "baddr": "",
        "buyerSq": args.buyerSq,
        "hp": "",
        "installed": "N",
        "ip": "",
        "location": args.location,
        "name": args.name,
        "regDate": "",
        "regId": "",
        "sshHost": "",
        "sshPort": str(yid),
        "status": "A",
        "yid": yid}
#boxes={}

def loadLock(ltype):
    with open("data/"+ltype+"type.json") as json_file:
        return json.load(json_file)
'''
for idx,p in enumerate(['a','b','c'],start=0):
    with open("data/"+p+"type.json") as json_file:
        d = json.load(json_file)
        boxes[p]=d
        # jsonstr = json.dumps(config['cabinet'])
        # print(jsonstr)
'''

cabinet=[]
label_start=65
for item in args.boxes:
    #print(item)
    row = loadLock(item)
    ritem={'depth':500}
    label_char = chr(label_start)
    boxList=[]
    for box  in row:
        if box.get('kind')!='A':

            box['label'] = label_char+box['label']
        boxList.append(box)
    ritem['box']=boxList
    cabinet.append(ritem)
    label_start+=1

postData = {'applebox':o2obox,'cabinet':cabinet}

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(postData)

r = requests.post('http://server:3000/v1/appleboxCreate', json=postData)

print(r.text)

if r.status_code==200 :
    ainfo = json.loads(r.text)
    pp.pprint(ainfo)
    os.system("python imp.py "+str(ainfo['yid']))
else:
    print('error')
