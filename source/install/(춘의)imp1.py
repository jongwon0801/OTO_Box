# /home/pi/Workspace/newapp/applelocker/imp1.py

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# encoding: utf-8
import os
import sys
import django
import json
import requests
import codecs

import re
import jwt
from django.conf import settings
sys.path.append("../") #path to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'appleapp.settings'
#django.setup()
from django.forms.models import model_to_dict
from annoying.functions import get_object_or_None


def testlist():
    rs = Applebox.objects.all()
    for v in rs:
        print(v.__dict__)
def testget():
    #rs = get_object_or_None(Applebox, yid=17)
    rs = Applebox.objects.get(yid=17)

    print(rs.__dict__)
def testinsert(applebox):
    applebox.save()
def testupdate():
    ap = Applebox(yid=17, name='상암동이야 ')
    ap.save(update_fields=["name"])
def testdelete():
    #ap = Applebox(pk=14)
    #ap.delete(ap)
    #try:
    Applebox.objects.get(yid=17).delete()
    #except:
    #    pass
def getApikey(ev):
        return jwt.encode(ev, 'ilovescotchyscotch', algorithm='HS256').decode('utf-8')
def run():
    #testdelete()
    #testupdate()
    #testlist()
    ##json.dumps(list(rs))
    #print(model_to_dict(rs))
    #print(rs.__dict__)
    #yid = int(os.uname()[1].split('-')[1])
    yid = int(sys.argv[1])
    #yid=10000
    Applebox.objects.all().delete()
    Locker.objects.all().delete()
    House.objects.all().delete()
    url = 'http://server/v1/AppleboxAll/'+str(yid)
    u = {'memberSq': 0, 'hp': '', 'name': ''}
    atoken = getattr(settings, "ATOKEN", None)
    resp = requests.get(url=url, params=None,headers={'Authorization': 'Bearer '+atoken})
    print(resp.text)
    data = json.loads(resp.text)

    print(data);
    cvalues = data['applebox']

    print(cvalues)

    print(json.dumps(cvalues['addr']))
    cvalues['addr'] = json.dumps(cvalues['addr'])


    print(cvalues)
    applebox = Applebox(**cvalues)


    #if True:
    #    return
    applebox.save()
    list = data['cabinet'];
    for item in list:
        boxes = item['box']
        for box in boxes:

            #print(box)
            #locker = Locker.objects.create(boxes)
            locker = Locker(**box)
            print(model_to_dict(locker))

            locker.save()

    if applebox.useType!='C':
        url = 'http://server/v1/House/' + str(yid)
        u = {'memberSq': 0, 'hp': '', 'name': ''}
        resp = requests.get(url=url, params=None, headers={'Authorization': 'Bearer ' + atoken})
        data = json.loads(resp.text)
        houses = data
        for item in houses:
            print(item);
            house = House(**item)
            house.save()

if __name__ == '__main__':
    django.setup()
    from applebox.models import Applebox,Locker,Property,House
    run()
