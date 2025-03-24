# /home/pi/Workspace/newapp/applelocker/syncdb_rfid.py


# -*- coding: utf-8 -*-
import os
import sys
import django
import json
import requests
import codecs
import logging

sys.path.append("../") #path to your settings file
os.environ['DJANGO_SETTINGS_MODULE'] = 'appleapp.settings'

logger = logging.getLogger('django')

logger.info('syncdb rfid')


def run():
    with connection.cursor() as cursor:

        cursor.execute('select max(modDate) modDate from applebox_rfid')
        row = cursor.fetchone()

    #print(row)


    requestProc(row[0])



def requestProc(modDate):

    print(modDate)
    url = 'http://server:3000/v1/Rfid'
    resp = requests.get(url=url, params={'modDate':modDate},headers={'Authorization':'Bearer '+settings.ATOKEN})
    print(resp)
    data = json.loads(resp.text)
    #print(resp.text)
    for item in data['data']:
        rfid = Rfid(**item)
        #print(item)
        try:
            rs = Rfid.objects.get(tagid=item['tagid'])
            rfid.save(force_update=True)
        except :
            rfid.save(force_insert=True)
        #print(rfid)
        #rfid.save()

if __name__ == '__main__':
    django.setup()
    from django.db import connection
    from django.conf import settings
    from applebox.models import Applebox,Locker,Rfid
    run()
