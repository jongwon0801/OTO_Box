# /home/pi/Workspace/newapp/applelocker/export.py

import os
import sys
import django
import json
import requests
import codecs
import time
import threading
sys.path.append("../") #path to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'appleapp.settings'
yid = int(os.uname()[1].split('-')[1])
#yid=10000
import pprint
from django.forms.models import model_to_dict
import argparse
import jwt
parser = argparse.ArgumentParser(description='서버에 데이타 보내기')
parser.add_argument('-t', '--tables',required=True,nargs='+', choices=['applebox', 'locker'], help='테이블명')
args = parser.parse_args()


def getApikey(ev):
    return jwt.encode(ev, 'ilovescotchyscotch', algorithm='HS256').decode('utf-8')


def run():
    for item in args.tables:
        if item=='applebox':
            abitem = Applebox.objects.get(yid=yid)

            #postData = {'applebox': o2obox, 'cabinet': cabinet}

            #pp = pprint.PrettyPrinter(indent=2)
            #pp.pprint(postData)
            u = {'memberSq': 0, 'hp': '', 'name': ''}
            r = requests.put('http://server:3000/v1/Applebox/'+str(yid), json=model_to_dict(abitem),headers={'Authorization': 'Bearer '+getApikey(u)})
            if r.status_code == 200:
                print('update success')
            else:
                print('update fail')

        elif item=='locker':
            list = Locker.objects.filter(yid=yid)

            u = {'memberSq': 0, 'hp': '', 'name': ''}
            rlist = []
            for locker in list:
                rlist.append(model_to_dict(locker))
            r = requests.put('http://server:3000/v1/Locker', json=rlist,
                             headers={'Authorization': 'Bearer ' + getApikey(u)})
            if r.status_code == 200:
                print('update success')
            else:
                print('update fail')

if __name__ == '__main__':
    django.setup()
    from applebox.models import Applebox, Locker
    from applelocker import LockerService
    run()

