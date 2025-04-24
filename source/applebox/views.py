# /home/pi/Workspace/newapp/applebox/views.py

# -*- coding: utf-8 -*-
from django.forms.models import model_to_dict
from django.shortcuts import render

# Create your views here.
import sys
from django.db.models import Count
from django.db import connection
from django.conf import settings
#from applebox.models import Applebox,AppleboxForm
from applebox.models import Notice,AppleboxForm, Applebox,Locker,LockerForm,Log,LogForm,Rfid,SaveLog,Push,TakeLog,Property,House,CodeTbl,Resident,Service
from django.http import HttpResponse
from django.http import JsonResponse, HttpResponseServerError
from django.forms.models import model_to_dict
import json
import jwt
import uuid
#import datetime
import random
from applelocker import LockerService,rs485,LockerEvent, ServiceMonitor
import platform
import os
import serial
from annoying.functions import get_object_or_None
import requests
import logging
import traceback
# Get an instance of a logger
import logging
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from dateutil import tz
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime, timezone,timedelta
from django.conf import settings
LOCKER_URL = getattr(settings, "LOCKER_URL", None)

import mysql.connector
import time
import fcntl
import struct

#import DongwonWallpadThread
#logger = logging.getLogger(__name__)
def log_except_hook(*exc_info):
    text = "".join(traceback.format_exception(*exc_info))
    logging.error("Unhandled exception: %s", text)

sys.excepthook = log_except_hook

import subprocess

from applebox.ir_check import IrCheck
from threading import Thread

#print(datetime.now(tz.gettz('Asia/Seoul')).strftime("%Y/%m/%d %H:%M"))
logger = logging.getLogger('django')

logger.info('start django server')

import socket
if len(sys.argv)>1 and  sys.argv[1]=='runserver' :
    def testLocker(portName):
        print(portName)
        try:

            b = LockerService.testStatus('/dev/' + portName)

            if b == True:
                '''
                process = subprocess.Popen(['sh','/home/pi/install/3.peripheral.sh', 'l='+portName], stdin=subprocess.PIPE,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE, shell=False)
                if process.returncode==0:
                    logger.info('script success')
                else:
                    logger.info('script fail')
                stream, err = process.communicate()
                '''
                subprocess.run(['/home/pi/install/3.peripheral.sh', 'l='+portName])
                time.sleep(2)
                b = LockerService.testStatus('/dev/hunes')
            return b

        except Exception as e:
            logger.error(e)
            raise e


    def checkLocker():
        try:

            return testLocker('ttyUSB0')

        except Exception as e:
            print(e)
            try:
                return testLocker('ttyUSB1')
            except Exception as e:
                print(e)
                raise e




    def get_ip_address(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', bytes(ifname[:15], 'utf-8'))
        )[20:24])




    try:

        LockerService.testStatus('/dev/hunes')
    except Exception as e:
        print(e)
        try:
            checkLocker()

        except Exception as e:
            print(e)
            #exit(2)
            print('locker controller failed')

    #print('locker controller test success');
    #url = 'http://server/v2/Things/' + data['thingsSq']




    try:
        yid = int(os.uname()[1].split('-')[1])
        lockerEvent = LockerEvent.LockerEvent(yid)
        lockerEvent.start()


    except Exception as e:
        #yid=10000
        print(e)
        exit(1)
        print('no yid!!!')
        #sys.exit(-1)
    '''
    try:
        requests.put(url=LOCKER_URL + '/v2/Ip/' + str(yid) + '/' + get_ip_address('eth0'))
    except Exception as e:
        print(e)
    '''


mIrSensor = IrCheck()
mIrSensor.start()
#from django.conf import settings
#PRIVATE_DIR = getattr(settings, "PRIVATE_DIR", None)
def my_random_string(string_length=10):
    """Returns a random string of length string_length."""
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:string_length]
def index(request):
    applebox = Applebox.objects.all().first()

    version= 1.0
    return HttpResponse("Welcome to %s:V%s"%(applebox,version))


def ProcessList(request):
    res=[
        #{'name':'키오스크', 'start':'ssh pi@localhost >>"sh home/pi/Workspace/kivymercury/applebox.sh"',
        # 'end':'pkill -9 -f /home/pi/Workspace/kivymercury/applebox.py','process':'pgrep -f /home/pi/Workspace/kivymercury/applebox.py'},
        #{'name': '웹서버',
        # 'start': 'nohup /home/pi/.virtualenvs/o2obox/bin/python /home/pi/Workspace/newapp/manage.py runserver 0.0.0.0:8000 &',
        # 'end': 'pkill -9 -f /home/pi/Workspace/newapp/manage.py','process':'pgrep -f /home/pi/Workspace/newapp/manage.py'},


        {'name':'리부트', 'start':'sudo reboot'},
        {'name': '시간동기화',
         'start': 'sudo ntpdate -u 211.233.84.186'},
        {'name': '모든 문열기',
         'start': 'sh /home/pi/Workspace/newapp/applelocker/ctrl.sh'},
        {'name': '비콘',
            'start': 'sudo systemctl restart ibeacon.service',
            'end': 'sudo systemctl stop ibeacon.service',
            'processCheck':ServiceMonitor.ServiceMonitor('ibeacon').is_active()
        },
        {'name': 'pir센서',
         'start': 'sudo systemctl restart pir.service',
         'end': 'sudo systemctl stop pir.service',
         'processCheck': ServiceMonitor.ServiceMonitor('pir').is_active()
         },
        {'name': 'cctv',
         'start': 'sudo systemctl restart motioneye',
         'end': 'sudo systemctl stop motioneye',
         'processCheck': ServiceMonitor.ServiceMonitor('motioneye').is_active()
         },
        {'name': '바코드',
         'start': 'sudo systemctl restart barcode.service',
         'end': 'sudo systemctl stop barcode.service',
         'processCheck': ServiceMonitor.ServiceMonitor('barcode').is_active()
         },
        {'name': 'reverse ssh',
         'start': 'sudo systemctl restart reversessh.service',
         'end': 'sudo systemctl stop reversessh.service',
         'processCheck': ServiceMonitor.ServiceMonitor('reversessh').is_active()
         },


    ]
    '''
    for item in res:
        if item.get('process'):
            process = subprocess.Popen(item['process'].split(), stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=False)
            out, err = process.communicate()
            item['processCheck']= (out.decode().strip()!='')
    '''
    return JsonResponse(res, safe=False)

'''
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json'  -d '["ssh", "-o", "StrictHostKeyChecking=no","-N","-T", "-R60001:localhost:22","root@server","-p","2222"]' 'http://localhost:11100/v1/ExecuteProcess'

curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json'  -d '["rm","/home/pi/.ssh/known_hosts"]' 'http://localhost:11100/v1/ExecuteProcess'
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json'  -d '["sudo","shutdown","-r","now"]' 'http://localhost:11055/v1/ExecuteProcess'
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json'  -d '["pkill","-9","python"]' 'http://localhost:11055/v1/ExecuteProcess'
'''
def ExecuteProcess(request):
    req = json.loads(request.body.decode("utf-8"))
    print(req)

    process = subprocess.Popen(req, stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)
    stream,err = process.communicate()
    logger.info(str(process.returncode))

    print(err.decode("utf-8"))
    #print(type(stream))
    return JsonResponse(
        {'returncode': str(process.returncode), 'out': stream.decode("utf-8"), 'error': err.decode("utf-8")}, json_dumps_params={'indent': 2})


    #os.system(' '.join(req))
    #return JsonResponse({})
def NoticeList(request):


    list = Notice.objects.filter(status='A')
    rs = []
    for item in list:
        rs.append(model_to_dict(item))
    return JsonResponse(rs, safe=False)


def PropertyList(request):

    result={}
    list = Property.objects.all()
    for item in list:

        result[item.name]=item.value

    return JsonResponse(result)

def ResidentReq(request):

    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.method=='POST': #입력
        #item = {'name': request.POST.get("name"), 'value': request.POST.get("value")}
        req = json.loads(request.body.decode("utf-8"))
        idata = Resident(**req)
        idata.modDate=iso_format(datetime.utcnow())
        try:

            idata.save(force_insert=True)
        except Exception as e:
            print(e);
            return JsonResponse({'success': False, 'errorCode': 505, 'message': 'error'}, status=505)
        return JsonResponse({})
    elif request.method=='GET': #목록
        list = Resident.objects.all()

        if request.GET.get('dong') :
            list=list.filter(dong=request.GET.get('dong'))
        if request.GET.get('ho') :
            list=list.filter(ho=request.GET.get('ho'))
        rs = []
        for item in list:
            rs.append(model_to_dict(item))
        return JsonResponse(rs, safe=False)
    return JsonResponse({}, status=404)

def PropertyReq(request):
    #print('bbbb', request.method)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.method=='POST': #입력
        #item = {'name': request.POST.get("name"), 'value': request.POST.get("value")}
        req = json.loads(request.body.decode("utf-8"))
        idata = Property(**req)
        try:

            idata.save(force_insert=True)
        except Exception as e:
            return JsonResponse({'success': False, 'errorCode': 505, 'message': 'error'}, status=505)
        return JsonResponse({})
    elif request.method=='GET': #목록
        list = Property.objects.all()
        rs = []
        for item in list:
            rs.append(model_to_dict(item))
        return JsonResponse(rs, safe=False)
    return JsonResponse({}, status=404)
    #return JsonResponse(result)

def PropertyItemReq(request,name):
    print('aaaaa',request.method)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    if request.method == 'PUT':  #
        req = json.loads(request.body.decode("utf-8"))
        try:

            udata = Property.objects.filter(name=name).first()
            udata.value=req.get('value')
            udata.save(force_update=True)
        except Exception as e:
            print(e);
            return JsonResponse({'success': False, 'errorCode': 505, 'message': 'error'}, status=505)
        return JsonResponse({})
    elif request.method=='DELETE': #삭제
        try:

            Property.objects.filter(name=name).first().delete()
        except Exception as e:
            return JsonResponse({'success': False, 'errorCode': 505, 'message': 'error'}, status=505)
        return JsonResponse({})
    elif request.method=='GET': #조회

        data = Property.objects.filter(name=name).first()
        # print(applebox)

        # print(settings.VERSION);
        if data:
            return JsonResponse(model_to_dict(data))
        else:
            return JsonResponse({},status=404)
    return JsonResponse({}, status=404)

def CodeTbls(request,gCode):

    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    result_list = CodeTbl.objects.filter(gCode=gCode)


    rs = []
    for item in result_list:
        rs.append(model_to_dict(item))
    return JsonResponse(rs,safe=False)

def NetworkCheck(request):
    if len(Push.objects.all()) == 0 :
        return JsonResponse({'status':True})
    else:
        return JsonResponse({'status': False})

def Reset(request):

    process = subprocess.Popen(['sudo', 'reboot'], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)
    return JsonResponse({})

def SignOut(request):

    return JsonResponse({})
def SignIn(request):

    #print('haha')
    #email = request.POST.get('email')


    req = json.loads(request.body.decode("utf-8"))
    password = req.get('password')

    #print(password)
    #e = Property.objects.get(name='email').value
    try:
        p = Property.objects.get(name='password').value

        #print(p)
        if password==p:

            #print(globals()['yid'])
            data = model_to_dict(Applebox.objects.filter()[0])

            data['systemDate']=iso_format(datetime.utcnow())
            #data['exp']= datetime.utcnow() + timedelta(minutes=5)
            return JsonResponse({'token': jwt.encode(data, JWTPWD, algorithm='HS256').decode('utf-8'),
                                     'name':data['name']})

        else:
            return JsonResponse({'success': False, 'errorCode': 404}, status=404)
    except Exception as e:
        print(e)
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)



def Install(request,yid):
    process = subprocess.Popen(['sudo', '/home/pi/install.sh', yid,'notlte'], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)

    stream = process.communicate()[0]
    if process.returncode == 0:
        process = subprocess.Popen(['sudo', 'reboot'], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)
        JsonResponse({})
    else:
        return JsonResponse({'error':'error'},status=500)
    '''
    if process.returncode==0:
        try:
            Applebox.objects.all().delete()
            Locker.objects.all().delete()
            House.objects.all().delete()
            url = 'http://server/v1/AppleboxAll/' + str(yid)
            u = {'memberSq': 0, 'hp': '', 'name': ''}
            resp = requests.get(url=url, params=None, headers={'Authorization': 'Bearer ' + getApikey(u)})
            data = json.loads(resp.text)


            cvalues = data['applebox']

            # print(cvalues)

            # print(json.dumps(cvalues['addr']))
            cvalues['addr'] = json.dumps(cvalues['addr'])
            applebox = Applebox(**cvalues)

            # if True:
            #    return
            applebox.save()
            list = data['cabinet'];
            for item in list:
                boxes = item['box']
                for box in boxes:
                    # print(box)
                    # locker = Locker.objects.create(boxes)
                    locker = Locker(**box)
                    print(model_to_dict(locker))

                    locker.save()

            url = 'http://server/v1/House/' + str(yid)
            u = {'memberSq': 0, 'hp': '', 'name': ''}
            resp = requests.get(url=url, params=None, headers={'Authorization': 'Bearer ' + getApikey(u)})
            data = json.loads(resp.text)
            houses = data
            for item in houses:
                print(item)
                house = House(**item)
                house.save()
            process = subprocess.Popen(['sudo', 'reboot'], stdin=subprocess.PIPE,
                                       stdout=subprocess.PIPE,
                                       stderr=subprocess.PIPE, shell=False)

            return JsonResponse({})
        except Exception as e:
            print(e)
            return JsonResponse({}, status=505)
    else:

        return JsonResponse({},status=505)

    '''
    #res = os.system("ping -c 1 smart.apple-box.kr")
    #ret['ping'] = res == 0




    #if applebox:
    #    return JsonResponse (model_to_dict(applebox));
        #return JsonResponse({'version': settings.VERSION, 'yid': applebox.yid, 'message':'hi !!','date':datetime.datetime.now()})
    #else :
    #    return JsonResponse(
    #        {'version': settings.VERSION, 'yid': None, 'message': 'os 명이 미설정 !!', 'date': datetime.datetime.now()},status=405)


def Config(request,osname, appversion):
    #if 'yid' in globals():
    #applebox = Applebox.objects.all().first()

    applebox = Applebox.objects.get(yid=globals()['yid'])
    #print(applebox)

    #print(settings.VERSION);

    if applebox:
        return JsonResponse (model_to_dict(applebox));
        #return JsonResponse({'version': settings.VERSION, 'yid': applebox.yid, 'message':'hi !!','date':datetime.datetime.now()})
    else :
        return JsonResponse(
            {'version': settings.VERSION, 'yid': None, 'message': 'os 명이 미설정 !!', 'date': datetime.now()},status=405)

def isLogin(request):
    try:
        bearer = request.META.get('HTTP_AUTHORIZATION')

        api_key = None
        if bearer:
            api_key = bearer.split(" ")[1]

            request.user = parseApikey(api_key)


            request.api_key= api_key


            return True
    except Exception as e:
        logger.exception('isLogin')
        return False
    return False

def AutosshStart(request,outport,inport):
    #ssh -o -N o2obox-tunnel
    #autossh -M 0 -o ServerAliveInterval=300 -R 42422:localhost:8000 root@125.209.200.159 -p 2222

    process = subprocess.Popen(['/home/pi/reversessh.sh',"start", outport,inport],stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,shell=False)

    #process.stdin.write(b'tmshdnxmfl\n')
    #process.stdin.flush()

    #stdout, stderr = process.communicate()
    #print(stdout)
    #print(stderr)
    #out = process.communicate()[0]
    #print(out.decode())
    return JsonResponse({'success': True})
    #return JsonResponse({'success': True})

def AutosshStop(request):
    process = subprocess.Popen(['sh', '/home/pi/reversessh.sh','stop'])
    return JsonResponse({'success': True})


def GetIp(request):
    #process = subprocess.Popen(["ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1"])

    process = subprocess.Popen("ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    out = process.communicate()[0]
    return JsonResponse({'ip': out.decode().strip()})

def NetworkChange(request):
    req = json.loads(request.body.decode("utf-8"))
    ret = {};

    process = subprocess.Popen(['sudo', 'sed','-i','8s/.*/'+req.get('server')+ ' server/','/etc/hosts'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)
    out = process.communicate()[0]
    process = subprocess.Popen(['sudo', 'sed', '-i', '9s/.*/' + req.get('vpnserver') + ' vpnserver/', '/etc/hosts'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)
    out = process.communicate()[0]
    process = subprocess.Popen(['sudo', 'sed', '-i', '10s/.*/' + req.get('homeserver') + ' homeserver/', '/etc/hosts'],
                               stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)
    out = process.communicate()[0]
    if req.get('networkType')=='static':
        print(req)
        ip= req.get("ip")
        ip=ip.replace('/', '\\/')
        '''
        
        '''
        '''
        process = subprocess.Popen(['bash', '/home/pi/install/2.network.sh',ip,req.get('gateway'),req.get('dns')], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=False)
        '''

        subprocess.run(['/home/pi/install/2.network.sh','type=static', 'sip='+req.get('server'), 'ip=' + ip, 'gip=' +req.get('gateway'), 'dns=' +req.get('dns'), 'vip=' + req.get('vpnserver'), 'hip=' + req.get('homeserver')])
    elif req.get('networkType')=='dynamic':
        subprocess.run(['/home/pi/install/2.network.sh','type=dynamic', 'sip=' + req.get('server'),
              'vip=' + req.get('vpnserver'), 'hip=' + req.get('homeserver')])



    return JsonResponse({'success':False})


def NetworkInfo(request):
    #process = subprocess.Popen(["ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1"])
    ret = {};

    filepath = '/etc/hosts'
    server=''
    temp = open(filepath, 'r').read().splitlines()
    for line in temp:
        data = line.strip().split()
        if len(data) == 2:
            # print(':'+data[1]+':')
            # print(data[0][0]=='#',data[1]=='server')
            if data[0][0] != '#' and data[1] == 'server':
                #server = data[0]
                ret['server'] = data[0]

            if data[0][0] != '#' and data[1] == 'homeserver':
                ret['homeserver'] = data[0]

            if data[0][0] != '#' and data[1] == 'vpnserver':

                ret['vpnserver'] = data[0]


        #print(data)

    #ret['server']=server
    process = subprocess.Popen("ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1",shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    out = process.communicate()[0]
    ret['ip']=out.decode().strip()

    process = subprocess.Popen("ip route | awk '/default/ { print $3 }'", shell=True,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    out = process.communicate()[0]
    ret['gatewayip'] = out.decode().strip()

    res = os.system("ping -c 1 server")
    ret['ping'] = res==0

    return JsonResponse(ret)

def AcceptNumber(request,yid,acceptNumber,status,usage):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    myboxs = Locker.objects.filter(yid=yid,acceptNumber=acceptNumber,status=status,usage=usage)

    rs=[]
    for row in myboxs:
        rs.append(model_to_dict(row, exclude=['pwd']))

    #print(rs)
    return JsonResponse({'success': True, 'data':rs})


def MyBox(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    pwd = request.GET.get('pwd')
    if pwd :

        '''
        if len(pwd)==6:
            houses = House.objects.filter(yid=yid,pwd=pwd)
            if len(houses)==0:
                myboxs=[]
            else:
                house = houses[0]
                myboxs=Locker.objects.filter(yid=yid, toDong=house.dong,toHo=house.ho, status='A')|Locker.objects.filter(yid=yid, toDong=house.dong,toHo=house.ho, status='X')
        else:

            myboxs = Locker.objects.filter(yid=yid,pwd=pwd,status='B')| Locker.objects.filter(yid=yid,pwd=pwd,status='A')|Locker.objects.filter(yid=yid,pwd=pwd,status='X')
        '''

        applebox = Applebox.objects.get(yid=yid)

        if applebox.useType=='A':

            pitem = Property.objects.filter(name='takepwd').first()

            if pitem and pitem.value==pwd:
                myboxs = Locker.objects.filter(yid=yid, status='A')
            else:
                myboxs = []
        else:
            houses = House.objects.filter(yid=yid, pwd=pwd)
            if len(houses)==0:
                myboxs = Locker.objects.filter(yid=yid, pwd=pwd, status='B') | Locker.objects.filter(yid=yid, pwd=pwd,
                                                                                                 status='A') | Locker.objects.filter(
                    yid=yid, pwd=pwd, status='X')
            else:
                house = houses[0]
                myboxs = Locker.objects.filter(yid=yid, toDong=house.dong, toHo=house.ho,
                                           status='A') | Locker.objects.filter(yid=yid, toDong=house.dong,
                                                                               toHo=house.ho, status='X')

    else:
        #myboxs = Locker.objects.filter(yid=yid, pwd=request.user['hp'], status='A') |Locker.objects.filter(yid=yid, pwd=request.user['hp'], status='X')
        myboxs=[]

    rs=[]
    cv = Property.objects.filter(name='controller_version').first()
    for row in myboxs:
        if row.status=='X':


            if cv and cv.value == '2':
                rs.append(model_to_dict( Locker.objects.get(yid=row.yid,jumper=row.jumper+1, serial=row.serial), exclude=[]))
            else:
                rs.append(model_to_dict(Locker.objects.get(yid=row.yid, jumper=row.jumper , serial=row.serial+1),
                                        exclude=[]))
        rs.append(model_to_dict(row, exclude=[]))

    #print(rs)
    return JsonResponse({'success': True, 'data':rs})

def MyLocker(request,dong,ho):
    #if globals()['yid'] != int(yid):
    #    return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    pwd = request.GET.get('pwd')
    if pwd :
        #if pwd[0:1]=='0':
        houses = House.objects.filter(dong=dong,ho=ho,pwd=pwd)

        if len(houses) >0:

            myboxs=Locker.objects.filter(toDong=dong,toHo=ho, status='A')|Locker.objects.filter(toDong=dong,toHo=ho, status='X')
        else:
            #myboxs = Locker.objects.filter(toDong=dong,toHo=ho,pwd=pwd,status='A')|Locker.objects.filter(toDong=dong,toHo=ho,pwd=pwd,status='X')
            #myboxs = []
            return JsonResponse({'success': False, 'message': 'no user', 'errorCode': 404},status=404)
    else:
        #myboxs = Locker.objects.filter(yid=yid, pwd=request.user['hp'], status='A') |Locker.objects.filter(yid=yid, pwd=request.user['hp'], status='X')
        myboxs=[]

    rs=[]
    cv = Property.objects.filter(name='controller_version').first()
    for row in myboxs:
        if row.status=='X':
            if cv and cv.value == '2':
                rs.append(model_to_dict( Locker.objects.get(jumper=row.jumper+1, serial=row.serial), exclude=['pwd']))
            else:
                rs.append(model_to_dict(Locker.objects.get(jumper=row.jumper, serial=row.serial +1), exclude=['pwd']))
        #rs.append(model_to_dict(row, exclude=['pwd']))
        rs.append(model_to_dict(row))

    #print(rs)
    return JsonResponse({'success': True, 'data':rs})

def Applebox1(request, yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not installed!!!', 'errorCode': 405}, status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.method == 'GET':  # 입력
        try:
            data = model_to_dict(Applebox.objects.get(yid=yid))
            data['addr'] = json.loads(data['addr'])
            return JsonResponse({'success': True, 'data': data})
        except Exception as e:

            return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)
    elif request.method == 'PUT':  # 입력
        try:
            req = json.loads(request.body.decode("utf-8"))
            data = Applebox.objects.get(yid=yid)
            data.addr=json.dumps(req['addr'])
            data.laundryFlag=req['laundryFlag']
            data.parcelFlag = req['parcelFlag']
            data.qrcodeFlag = req['qrcodeFlag']
            data.name= req.get('name')
            data.buyerSq = req.get('buyerSq')
            data.save(force_update=True)
            #data['addr'] = json.loads(data['addr'])
            return JsonResponse({'success': True, 'data': model_to_dict(data)})
        except Exception as e:
            print(e)
            return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)



def Cmd(request):


    jumper = request.GET.get('jumper')
    if jumper == None:
        jumper = '1'
    jumper = int(jumper)
    cmd = request.GET.get('cmd')



    try:

        if cmd=='OPEN' :
            p = LockerService.openDoorSimple(jumper, int(request.GET.get('serial')), getDeviceName(jumper))
        elif cmd=='INIT' :
            p = LockerService.initDoor(jumper, getDeviceName(jumper))
        elif cmd=='STATUS' :
            p = LockerService.statusBoard(jumper, getDeviceName(jumper))  # 상태


        if p:
            rs = [p[0],p[1],p[2],[p[3],'{:08b}'.format(p[3])[::-1]],[p[4],'{:08b}'.format(p[4])[::-1]]]
            return JsonResponse({'success': True, 'data': rs})
        else :
            return JsonResponse({'success': True, 'data': None})
    except serial.serialutil.SerialException as e:
        logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 402, 'message': 'controller connection error'}, status=402)
    except Exception as e :
        logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)
'''
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I' -d '{}' 'http://smart.apple-box.kr:8000/v1/Status/10000'

'''
def Status(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    rs =[]

    try:
        cv = Property.objects.filter(name='controller_version').first()
        if cv and cv.value == '2':
            ds = []
            for j in Locker.objects.raw(
                    'SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null and jumper>0 and yid=%d'%int(yid)):
                # p = LockerService.statusBoard(j.jumper)
                ds.append(j.jumper)
            p = LockerService.statusSensors(ds)  # 상태

            for index, item in enumerate(ds):
                ritem = p[index]

                if ritem:

                    closed = rs485.isOn(ritem, 1)
                    #sstatus = rs485.isOn(ritem, 9)
                    rs.append({'jumper': item, 'serial': 1, 'closed': closed,'isSensing':ritem[4]==0})
                else:
                    rs.append({'jumper': item, 'serial': 1, 'closed': True, 'isSensing': False})
            return JsonResponse({'success': True, 'data': rs})
        else:
            for j in Locker.objects.raw('SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null and jumper > 0 and yid=%d'%int(yid)):
                p = LockerService.statusBoard(j.jumper, getDeviceName(j.jumper))
                #p = [0,0,0,0,0,0,0,0]
                #p = p*2

                if p:
                    for i in range(1, 17):
                        closed = rs485.isOn(p, i)
                        rs.append({'jumper': j.jumper, 'serial': i, 'closed': closed})
            return JsonResponse({'success': True, 'data': rs})
    except serial.serialutil.SerialException as e:
        logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 402, 'message': 'controller connection error'}, status=402)
    except Exception as e :
        logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)
def Sensor(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    rs =[]

    try:
        ds=[]
        for j in Locker.objects.raw(
                'SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null and jumper>0'):
            # p = LockerService.statusBoard(j.jumper)
            ds.append(j.jumper)
        p = LockerService.statusSensors(ds)  # 상태

        for i in p:
            closed = rs485.isOn(i, 1)
            rs.append({'jumper': j.jumper, 'serial': i[0], 'closed': closed})
        return JsonResponse({'success': True, 'data': rs})
    except serial.serialutil.SerialException as e:
        logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 402, 'message': 'controller connection error'}, status=402)
    except Exception as e :
        logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)


def StatusServer(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    try :

        url = 'http://server'

        resp = requests.get(url=url,timeout=5)
        #print(resp.text)
        if resp.status_code == 200:
            #data = json.loads(resp.text)
            return JsonResponse({'result':resp.text})

        else :
            #return Response
            #return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
            return HttpResponse(resp.text, status=resp.status_code)
    except Exception as e:
        #logger.exception('GetPincode')
        print(e)
        return JsonResponse({'success': False, 'errorCode':600, 'message':str(e)} ,status=511)


def parseApikey(apikey):
    if apikey:
        r = jwt.decode(apikey, JWTPWD, algorithms=['HS256'])

        if r.get('yid')== globals()['yid']:
            return r
    return None
def MakePassword(request, yid):
    logger.info(request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!', 'errorCode': 405}, status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)
    try:

        req = json.loads(request.body.decode("utf-8"))
        pwd = __getPwd(req.get('pwd'), 5)
        return JsonResponse({'success': True, 'data':{'pwd':pwd}})

    except Exception as e :
        logger.exception(e)
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)


'''
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I' -d '{
  "yid": 17,
  "jumper": 2,
  "serial": 1,
  "hp": "01068115228",
  "pwd": "0000"
}' 'http://localhost:8000/v1/OpenToTake/17'
'''


def OpenToTake(request, yid):
    logger.info(request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)
    try:
        user = request.user
        api_key =request.api_key
        #try:
        req = json.loads(request.body.decode("utf-8"))

        #print('req',req)
        lockerInfo = Locker.objects.get(yid=req['yid'],jumper=req['jumper'], serial=req['serial'])
        #lockerInfo = Locker.objects.get(yid=req['yid'], jumper=req['jumper'], serial=req['serial'])

        #다시 열기 기능 없음
        #if  lockerInfo.status == u'B' and lockerInfo.pwd == req['pwd']:
        #    LockerService.openDoor(req['jumper'], req['serial'])
        #    return JsonResponse({'success': True, 'data': req})

        if lockerInfo.status == u'A'  or lockerInfo.status == u'X':

            #applebox = Applebox.objects.get(yid=yid)

            if lockerInfo.pwd == req['pwd']:

                if LockerService.openDoor(req['jumper'], req['serial'], getDeviceName(req['jumper'])):
                    #lockerInfo.saveDate = iso_format(datetime.datetime.utcnow())
                    #slog = SaveLog.objects.filter(uuid=req['uuid']).first()
                    if lockerInfo.status == 'X':

                        cv = Property.objects.filter(name='controller_version').first()

                        if cv and cv.value == '2':
                            LockerService.openDoor(req['jumper']+1, req['serial'] , getDeviceName(req['jumper']))
                            lockerInfo1 = Locker.objects.get(yid=req['yid'], jumper=req['jumper']+1, serial=req['serial'] )
                            lockerInfo1.status = 'B'
                            lockerInfo1.save(update_fields=['status'])
                        else:
                            LockerService.openDoor(req['jumper'] , req['serial']+1, getDeviceName(req['jumper']))
                            lockerInfo1 = Locker.objects.get(yid=req['yid'], jumper=req['jumper'],
                                                             serial=req['serial']+1)
                            lockerInfo1.status = 'B'
                            lockerInfo1.save(update_fields=['status'])

                    lockerInfo.api_key = api_key
                    lockerInfo.status = 'E'
                    lockerInfo.price = req.get('price')
                    lockerInfo.usage=req.get('usage')
                    #lockerInfo.pwd=None
                    #lockerInfo.save(update_fields=['status', 'saveDate', 'api_key'])  # 특정한 필드 갱신
                    lockerInfo.save(update_fields=['status',  'api_key','usage'])  # 특정한 필드 갱신

                    abdata = Applebox.objects.get(yid=yid)
                    pdata = model_to_dict(lockerInfo)
                    #pdata['usage']=req.get('usage')
                    pdata['regDate'] = iso_format(datetime.utcnow())


                    #oldtoHp = lockerInfo.toHp


                    #if req.get('toHp'):
                    #    pdata['toHp']= req.get('toHp')
                    del pdata['id']
                    del pdata['step']
                    if pdata.get('sensor'):
                        del pdata['sensor']
                    if req.get('toHp'):
                        pdata['toHp']=req.get('toHp')
                    TakeLog(**pdata).save()
                    del pdata['api_key']

                    if abdata.useType!='A':
                        pdata['kind'] = 'B'  #
                        pdata['boxName'] = abdata.name
                        if req.get('toHp'):
                            pdata['toHp']=req.get('toHp')
                        if req.get('usage'):
                            pdata['usage']=req['usage']
                        pushData = {'command': '/v1/Locker/open_to_take', 'api_key': api_key, 'data': pdata}

                        wpdata = lockerEvent.getWallpad('out', lockerInfo)

                        if lockerEvent.sendWallpad(wpdata) == False:
                            lockerEvent.insertPush('2', wpdata)

                        if lockerEvent.sendPush(pushData, True) == False:
                            lockerEvent.insertPush('1',pushData)
                    return JsonResponse({'success': True, 'data': pdata})
                else:
                    logger.error('열기실패')
                    logger.error(req);
                    return JsonResponse({'success': False, 'errorCode': 402, 'message': '열수 없습니다. 다시한번 시도해주세요.[내부에러]'},
                                        status=402)
            else:
                logger.error('패스워드실패')
                logger.error(req);
                return JsonResponse({'success': False, 'errorCode': 401, 'message': '패스워드가 틀립니다. 다시한번 입력해주세요.'},
                                    status=401)
        elif  lockerInfo.pwd == req['pwd']:
            return JsonResponse({'success': False, 'errorCode': 409, 'message': '이미 찾아갔습니다.'}, status=409)
        else:
            logger.info('열기실패')

            return JsonResponse({'success': False, 'errorCode': 400, 'message': '열 수 있는 상태가 아닙니다.'}, status=400)
    except Exception as e :
        logger.exception(e)
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)



'''
curl -X POSpplication/json' --header 'Accept: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I' -d '{
  "yid": 17,
  "jumper": 2,
  "serial": 1,
  "saveHp": "01068115228",
  "saveName": "홍길동",
  "toName": "홍성철",
  "toHp": "01068115228",
  "usage": "B",
  "things": {
    "content": "ddddd",
    "things": {
      "upper_cnt": 0,
      "down_cnt": 0,
      "etc_cnt": 0
    }
  }
}' 'http://localhost:8000/v1/OpenToSave/17'
'''

def iso_format(dt):
    try:
        utc = dt + dt.utcoffset()
    except TypeError as e:
        utc = dt
    isostring = datetime.strftime(utc, '%Y-%m-%dT%H:%M:%S.{0}Z')
    ms = int(round(utc.microsecond / 1000.0))
    if ms < 100:
        ms = ms + 100
    return isostring.format(ms)

def TestOpenAll(request):
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)

    resData = []
    try :
        #print(0)
        user = request.user
        api_key = request.api_key


        req = json.loads(request.body.decode("utf-8"))

        controller_version = req.get('controller_version')
        startController = req.get('startController')
        startPort = req.get('startPort')
        endController = req.get('endController')


        portName=None
        if req.get('portName'):
            portName='/dev/'+req.get('portName')
        if startPort:
            ret = LockerService.openDoor(startController, startPort,portName)
            resData.append({'controller':startController,'port':startPort,'result':ret})
        else:
            i=startController
            if controller_version=='1':
                while i<= endController :
                    for j in range(16):
                        ret = LockerService.openDoor(i, j+1,portName )
                        resData.append({'controller': i, 'port': j+1, 'result': ret})
                    i +=1
            else:
                while i<= endController :
                    ret = LockerService.openDoor(i, 1 ,portName)
                    resData.append({'controller': i, 'port':  1, 'result': ret})
                    i +=1


    except Exception as e :
        logger.exception('TestOpenAll')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)

    return JsonResponse({'success': True,'data':resData})
'''
#import uuid

'''
def OpenToSave(request,yid):
    logger.info(request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)
    try :
        #print(0)
        user = request.user
        api_key = request.api_key
        print(request.body)

        req = json.loads(request.body.decode("utf-8"))
        #print(req)
        lockerInfo = Locker.objects.get(yid=req['yid'],jumper=req['jumper'],serial=req['serial'])
        #print(3)
        if lockerInfo.status == u'B' or lockerInfo.status == u'G':
            if LockerService.openDoor(lockerInfo.jumper, lockerInfo.serial, getDeviceName(lockerInfo.jumper)):
                #now = datetime.datetime.now()
                abdata = Applebox.objects.get(yid=yid)

                #saveDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                saveDate=iso_format(datetime.utcnow())
                #datetime.now().strftime('%a, %d %b %Y %H: %M: %S')

                pwd = str(random.randrange(10000, 100000, 3))
                while True:
                    fdata = Locker.objects.filter(pwd=pwd).first()
                    if fdata is None:
                        break
                    pwd = str(random.randrange(10000, 100000, 3))
                #pwd='19159'

                #
                lockerInfo.saveHp = req['saveHp']
                lockerInfo.saveName = req['saveName']
                lockerInfo.saveDate = saveDate


                lockerInfo.status='D'
                lockerInfo.pwd=pwd
                lockerInfo.api_key=api_key
                if req.get('usage') =='H' or  req.get('usage') =='C': #ladunryapp 이 세탁물 보관일때

                    lockerInfo.toName = Property.objects.get(name='laundryName').value
                    lockerInfo.toHp = Property.objects.get(name='laundryHp').value
                else:
                    lockerInfo.toName = req.get('toName', None)
                    lockerInfo.toHp = req['toHp']
                lockerInfo.toDong = req.get('toDong', None)
                lockerInfo.toHo = req.get('toHo', None)
                lockerInfo.usage = req.get('usage')
                lockerInfo.thingsSq = req.get('thingsSq')
                lockerInfo.things = req.get('things')
                lockerInfo.price = req.get('price',0)
                lockerInfo.boxName = abdata.name
                lockerInfo.uuid= my_random_string(30)
                lockerInfo.step='A'
                lockerInfo.save(update_fields=['saveHp','saveName','status','saveDate','api_key','pwd','toName','toHp','toDong','toHo','usage','thingsSq','boxName','uuid','step','price'])

                applebox = Applebox.objects.all().first()
                if ['usage']=='A':


                    if applebox.useType!='C':
                        rdata = {'yid':applebox.pyd, 'dong':req.get('toDong'),'ho':req.get('toHo'),'hp':req.get('toHp'),'modDate':saveDate}
                        idata = Resident(**rdata)
                        try:

                            idata.save(force_insert=True)
                        except Exception as e:
                            print(e)
                pdata = model_to_dict(lockerInfo)
                del pdata['id']
                del pdata['step']
                if pdata.get('sensor'):
                    del pdata['sensor']
                SaveLog(**pdata).save()

                if applebox.useType!='A': #local
                    del pdata['api_key']

                    pdata['boxName'] =abdata.name
                    pdata['pincodeSq'] = req.get('pincodeSq')

                    pushData = {'command': '/v1/Locker/open_to_save', 'api_key': api_key, 'data': pdata}
                    print(lockerInfo);
                    wpdata = lockerEvent.getWallpad('in', lockerInfo)
                    #doPrint(lockerInfo)
                    if lockerEvent.sendWallpad(wpdata) == False:
                        lockerEvent.insertPush('2',wpdata)
                    if lockerEvent.sendPush(pushData,True)==False:
                        lockerEvent.insertPush('1',pushData)
                return JsonResponse({'success': True, 'data':pdata})


            else:
                logger.error('열기실패')
                logger.error(req);
                return JsonResponse({'success': False, 'errorCode': 402, 'message': '열기 실패. 다시 시도해주세요'}, status=402)
        else:
            return JsonResponse({'success': False, 'errorCode': 400, 'message': 'Current status is not B.'},status=400)
    except Exception as e :
        logger.exception('OpenToSave')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)

def __getPwd(apend, tlen):

    if apend:
        pass
    else:
        apend=''
    alen = len(apend)
    if alen >= tlen:
        return apend
    pwd = str(random.randrange(pow(10,tlen-alen-1), pow(10,tlen-alen), 3))+apend
    while True:
        fdata = Locker.objects.filter(pwd=pwd).first()
        if fdata is None:
            break
        pwd = str(random.randrange(pow(10, tlen - alen - 1), pow(10, tlen - alen), 3))+apend
    return pwd
def OpenToSaveAll(request,yid):

    #logger.info('saveall',request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)
    try :
        #print(0)
        user = request.user
        api_key = request.api_key
        print(request.body)

        req = json.loads(request.body.decode("utf-8"))
        #print(req)
        lockerInfo = Locker.objects.get(yid=req['yid'],jumper=req['jumper'],serial=req['serial'])
        if LockerService.isOn(lockerInfo.jumper, lockerInfo.serial , getDeviceName(req['jumper'])): # closed

            if req.get('status')=='X':

                cv = Property.objects.filter(name='controller_version').first()

                if cv and cv.value == '2':
                    lockerInfo1 = Locker.objects.get(yid=req['yid'], jumper=req['jumper']+1, serial=req['serial'])
                    lockerInfo1.status='X'
                    lockerInfo1.saveHp = ''
                    lockerInfo1.toHp=''
                    lockerInfo1.toDong = ''
                    lockerInfo1.toHo = ''
                    lockerInfo1.pwd=None
                    lockerInfo1.save(update_fields=['status','toHp','saveHp','toHp','toDong','toHo','pwd'])
                else:
                    lockerInfo1 = Locker.objects.get(yid=req['yid'], jumper=req['jumper'] , serial=req['serial']+1)
                    lockerInfo1.status = 'X'
                    lockerInfo1.saveHp = ''
                    lockerInfo1.toHp = ''
                    lockerInfo1.toDong = ''
                    lockerInfo1.toHo = ''
                    lockerInfo1.pwd = None
                    lockerInfo1.save(update_fields=['status', 'toHp', 'saveHp', 'toHp', 'toDong', 'toHo', 'pwd'])

            abdata = Applebox.objects.get(yid=yid)

            #saveDate = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            saveDate=iso_format(datetime.utcnow())
            #datetime.datetime.now().strftime('%a, %d %b %Y %H: %M: %S')
            '''
            pwd = str(random.randrange(10000, 100000, 3))
            while True:
                fdata = Locker.objects.filter(pwd=pwd).first()
                if fdata is None:
                    break
                pwd = str(random.randrange(10000, 100000, 3))
            #pwd='19159'
            '''

            pwd= __getPwd(req.get('pwd'),5)

            #
            lockerInfo.saveHp = req['saveHp']
            lockerInfo.saveName = req['saveName']
            lockerInfo.saveDate = saveDate

            if req.get('status')=='X':
                lockerInfo.status='X'
            else:
                lockerInfo.status='A'
            lockerInfo.pwd=pwd
            lockerInfo.api_key=api_key
            #if req.get('usage') =='H' or  req.get('usage') =='C': #ladunryapp 이 세탁물 보관일때

            #    lockerInfo.toName = Property.objects.get(name='laundryName').value
            #    lockerInfo.toHp = Property.objects.get(name='laundryHp').value
            #else:

            lockerInfo.toName = None
            lockerInfo.toHp = None
            if req.get('usage') == 'H':
                service = Service.objects.filter(kind='A').first()
                if service:
                    lockerInfo.toName = service.name
                    lockerInfo.toHp = service.hp
            if lockerInfo.toHp==None:
                lockerInfo.toName = req.get('toName', None)
                lockerInfo.toHp = req['toHp']
            lockerInfo.toDong = req.get('toDong', None)
            lockerInfo.toHo = req.get('toHo', None)
            lockerInfo.usage = req.get('usage')
            lockerInfo.thingsSq = req.get('thingsSq')
            lockerInfo.things = req.get('things')
            lockerInfo.price = req.get('price',0)
            lockerInfo.acceptNumber = req.get('acceptNumber',None)

            lockerInfo.boxName = abdata.name
            lockerInfo.uuid= my_random_string(30)
            lockerInfo.step='A'
            lockerInfo.save(force_update=True, update_fields=['saveHp','saveName','status','saveDate','api_key','pwd','toName','toHp','toDong','toHo','usage','thingsSq','boxName','uuid','step','price','acceptNumber'])


            pdata = model_to_dict(lockerInfo)
            del pdata['id']
            del pdata['step']
            if pdata.get('sensor'):
                del pdata['sensor']
            SaveLog(**pdata).save()
            del pdata['api_key']


            if abdata.useType!='A':
                pdata['boxName'] =abdata.name
                pdata['pincodeSq'] = req.get('pincodeSq')
                pdata['shopSq'] = req.get('shopSq')
                pushData = {'command': '/v1/Locker/open_to_save_all', 'api_key': api_key, 'data': pdata}
                #print(lockerInfo);
                wpdata = lockerEvent.getWallpad('in', lockerInfo)

                if lockerEvent.sendWallpad(wpdata) == False:
                    lockerEvent.insertPush('2',wpdata)
                if lockerEvent.sendPush(pushData,True)==False:
                    lockerEvent.insertPush('1',pushData)
                #if lockerInfo.usage=='F':
                #    doPrint(lockerInfo)
            return JsonResponse({'success': True, 'data':pdata})

        else:
            return JsonResponse({'success': False, 'errorCode': 409, 'message': '락커가 열려있습니다.'}, status=409)

    except Exception as e :
        logger.exception('OpenToSaveAll')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)

def ParcelPost(request):
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)
    user = request.user
    #api_key = request.api_key
    #print(request.body)

    data = json.loads(request.body.decode("utf-8"))

    print(data)
    try :

        #url = 'http://smart.apple-box.kr:3000/v1/Pincode/'+pincode
        #url = 'http://172.24.1.95:3000/v1/Pincode/' +yid+'/'+ pincode
        #url = 'http://172.24.1.95:3000/v1/Pincode/' + yid + '/' + pincode
        url = 'http://server/v2/Things/'+data['thingsSq']

        resp = requests.get(url=url,headers={'Authorization': 'Bearer ' + settings.ATOKEN})
        if resp.status_code == 200:
            sdata = resp.json()
            print(sdata['status'])
            if sdata['status']=='A':

                b = parcelPrint(sdata)
                print(b)
                if b==True:
                    resp = requests.put(url = 'http://server/v2/ThingsParcel/'+data['thingsSq'], headers={'Authorization': 'Bearer ' + settings.ATOKEN})

                    print(resp.text)
                    #if resp.status_code==200
                    return JsonResponse({})

                else:
                    return JsonResponse({'error': 'print error1'}, status=502)
            else:
                return JsonResponse({'error': 'already print error1'}, status=501)
        else :
            #return Response
            #return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
            return HttpResponse(resp.text, status=resp.status_code)
    except Exception as e:
        logger.exception('GetPincode')
        return JsonResponse({'success': False, 'errorCode':600, 'message':str(e)} ,status=600)


    '''
    from PIL import Image, ImageDraw, ImageFont
    from escpos import config
    font_ = ImageFont.truetype('/home/pi/kivy/kivy/data/fonts/NanumGothic.ttf', 25)

    base = Image.new('RGB', (320, 360), color=(255, 255, 255))

    d = ImageDraw.Draw(base)

    d.text((0, 10), '여행자보관함 사용번호', font=font_, fill=(0, 0, 0))
    d.text((0, 40), '보관함명: ' + data.boxName, font=font_, fill=(0, 0, 0))
    d.text((0, 70), 'Date: ' + datetime.now(tz.gettz('Asia/Seoul')).strftime("%Y/%m/%d %H:%M"), font=font_,
           fill=(0, 0, 0))
    d.text((0, 100), 'User: ' + data.saveHp, font=font_, fill=(0, 0, 0))
    d.text((0, 130), 'Service: 개인보관함', font=font_, fill=(0, 0, 0))
    d.text((0, 160), 'Locker No: ' + data.label, font=font_, fill=(0, 0, 0))
    d.text((0, 190), 'Fee: ₩' + str(data.price), font=font_, fill=(0, 0, 0))
    d.text((0, 220), 'Password: ' + data.pwd, font=font_, fill=(0, 0, 0))
    base.save('print.jpg')
    '''
    process = subprocess.Popen(['lp', '-o', 'orientation-requested=4', '-o', 'fit-to-page', '-o', 'media=Custom.4x8in', '-o', 'media=*w4h8','print.jpg'], stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=False)

    stream = process.communicate()[0]
    if process.returncode == 0:
        JsonResponse({})
    else:
        return JsonResponse({'error': 'error'}, status=500)
    return JsonResponse({'success': True})


def parcelPrint(data):

    '''
    process = subprocess.Popen(
        ['lp', '-o', 'orientation-requested=4', '-o', 'media=Custom.4x7.93in', '-o', 'fit-to-page' ,'/home/wikibox/print.jpg'], shell=False, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    stream = process.communicate()[0]
    if process.returncode == 0:
        return True
    else:
        return False
    '''


    #data = sdata['things']
    try:
        #if data.usage=='B': # 짐캐리보관
        #    pass


        from dateutil import tz

        from escpos import config
        font_t = ImageFont.truetype('/home/pi/kivy/kivy/data/fonts/NanumGothic.ttf', 25)
        font_ = ImageFont.truetype('/home/pi/kivy/kivy/data/fonts/NanumGothic.ttf', 20)
        from barcode import Code39
        from barcode.writer import ImageWriter
        base = Image.new('RGB', (500, 520), color=(255, 255, 255))
        from datetime import datetime

        ean = Code39('abcdedf', writer=ImageWriter())
        ean.save('ean13_barcode')
        bc = Image.open("ean13_barcode.png")

        width, height = bc.size
        base.paste(bc, (0, 250))
        d = ImageDraw.Draw(base)
        applebox = Applebox.objects.filter().first()
        d.text((0, 10), applebox.name, font=font_t, fill=(0, 0, 0))
        d.text((0, 40), '보낸이:' + data['things']['fromAddr']['name'] + '(' + data['things']['fromAddr']['hp'] + ')',
               font=font_, fill=(0, 0, 0))
        #d.text((0, 70), data['things']['fromAddr']['roadAddrPart1'] + '' + data['things']['fromAddr']['roadAddrPart2'],
        #               font=font_, fill=(0, 0, 0))
        draw_word_wrap(d,
                       data['things']['fromAddr']['roadAddrPart1'] + '' + data['things']['fromAddr']['roadAddrPart2']+' '+data['things']['fromAddr']['detail'],
                       0,
                       70,
                       500, fill=(0, 0, 0), font=font_)

        #d.text((0, 100), data['things']['fromAddr']['detail'], font=font_, fill=(0, 0, 0))
        # d.text((0, 70), 'Date: ' + datetime.now(tz.gettz('Asia/Seoul')).strftime("%Y/%m/%d %H:%M"), font=font_, fill=(0, 0, 0))
        # d.text((0, 100), 'User: ', font=font_, fill=(0, 0, 0))
        # d.text((0, 130), 'Service: 개인보관함', font=font_, fill=(0, 0, 0))
        # d.text((0, 160), 'Locker No: ', font=font_, fill=(0, 0, 0))
        # d.text((0, 190), 'Fee: ₩', font=font_, fill=(0, 0, 0))
        # d.text((0, 220), 'Password: ', font=font_, fill=(0, 0, 0))
        d.text((0, 130), '보낸이:' + data['things']['toAddr']['name'] + '(' + data['things']['toAddr']['hp'] + ')',
               font=font_, fill=(0, 0, 0))
        #d.text((0, 160), data['things']['toAddr']['roadAddrPart1'] + '' + data['things']['toAddr']['roadAddrPart2'],
        #       font=font_, fill=(0, 0, 0))
        #d.text((0, 190), data['things']['toAddr']['detail'], font=font_, fill=(0, 0, 0))
        draw_word_wrap(d,
                       data['things']['toAddr']['roadAddrPart1'] + '' + data['things']['toAddr'][
                           'roadAddrPart2'] + ' ' + data['things']['toAddr']['detail'],
                       0,
                       160,
                       500, fill=(0, 0, 0), font=font_)


        base.save('print.jpg')



        c = config.Config()
        p = c.printer()
        p.image("print.jpg")

        p.cut()
        return True
    except Exception as e:
        logger.error(e);

    return False
def draw_word_wrap(draw, text,
                   xpos=0, ypos=0,
                   max_width=130,
                   fill=(0,0,0),
                   font=ImageFont.truetype('/home/pi/kivy/kivy/data/fonts/NanumGothic.ttf', 25)):
    '''Draw the given ``text`` to the x and y position of the image, using
    the minimum length word-wrapping algorithm to restrict the text to
    a pixel width of ``max_width.``
    '''
    text_size_x, text_size_y = draw.textsize(text, font=font)
    remaining = max_width
    space_width, space_height = draw.textsize(' ', font=font)
    # use this list as a stack, push/popping each line
    output_text = []
    # split on whitespace...
    for word in text.split(None):
        word_width, word_height = draw.textsize(word, font=font)
        if word_width + space_width > remaining:
            output_text.append(word)
            remaining = max_width - word_width
        else:
            if not output_text:
                output_text.append(word)
            else:
                output = output_text.pop()
                output += ' %s' % word
                output_text.append(output)
            remaining = remaining - (word_width + space_width)
    for text in output_text:
        draw.text((xpos, ypos), text, font=font, fill=fill)
        ypos += text_size_y

def PrintReceipt(request):

    #logger.info('saveall',request.body)
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)
    user = request.user
    api_key = request.api_key
    print(request.body)

    req = json.loads(request.body.decode("utf-8"))
    # print(req)
    data = Locker.objects.get(yid=req['yid'], jumper=req['jumper'], serial=req['serial'])

    try:
        #if data.usage=='B': # 짐캐리보관
        #    pass

        if data.usage == 'F':  # 개인보관

            from PIL import Image, ImageDraw, ImageFont
            from escpos import config
            font_ = ImageFont.truetype('/home/pi/kivy/kivy/data/fonts/NanumGothic.ttf', 25)

            base = Image.new('RGB', (320, 360), color=(255, 255, 255))

            d = ImageDraw.Draw(base)

            d.text((0, 10), '보관함 사용번호', font=font_, fill=(0, 0, 0))
            d.text((0, 40), '보관함명: '+data.boxName, font=font_, fill=(0, 0, 0))
            d.text((0, 70), 'Date: ' + datetime.now(tz.gettz('Asia/Seoul')).strftime("%Y/%m/%d %H:%M"), font=font_, fill=(0, 0, 0))
            d.text((0, 100), 'User: '+data.saveHp, font=font_, fill=(0, 0, 0))
            d.text((0, 130), 'Service: 개인보관함', font=font_, fill=(0, 0, 0))
            d.text((0, 160), 'Locker No: '+data.label, font=font_, fill=(0, 0, 0))
            d.text((0, 190), 'Fee: ₩'+str(data.price), font=font_, fill=(0, 0, 0))
            d.text((0, 220), 'Password: '+data.pwd, font=font_, fill=(0, 0, 0))
            base.save('print.jpg')
            c = config.Config()
            p = c.printer()
            p.image("print.jpg")
            p.cut()
    except Exception as e:
        logger.error(e);
        return JsonResponse({'success': False, 'errorCode': 409, 'message': 'print error'}, status=409)
    return JsonResponse({'success': True})

def doPrint(data):

    try:
        #if data.usage=='B': # 짐캐리보관
        #    pass

        if data.usage == 'F':  # 개인보관

            from PIL import Image, ImageDraw, ImageFont
            from escpos import config
            font_ = ImageFont.truetype('/home/pi/kivy/kivy/data/fonts/NanumGothic.ttf', 25)

            base = Image.new('RGB', (320, 360), color=(255, 255, 255))

            d = ImageDraw.Draw(base)

            d.text((0, 10), '여행자보관함 사용번호', font=font_, fill=(0, 0, 0))
            d.text((0, 40), '보관함명: '+data.boxName, font=font_, fill=(0, 0, 0))
            d.text((0, 70), 'Date: ' + datetime.now(tz.gettz('Asia/Seoul')).strftime("%Y/%m/%d %H:%M"), font=font_, fill=(0, 0, 0))
            d.text((0, 100), 'User: '+data.saveHp, font=font_, fill=(0, 0, 0))
            d.text((0, 130), 'Service: 개인보관함', font=font_, fill=(0, 0, 0))
            d.text((0, 160), 'Locker No: '+data.label, font=font_, fill=(0, 0, 0))
            d.text((0, 190), 'Fee: ₩'+str(data.price), font=font_, fill=(0, 0, 0))
            d.text((0, 220), 'Password: '+data.pwd, font=font_, fill=(0, 0, 0))
            base.save('print.jpg')
            c = config.Config()
            p = c.printer()
            p.image("print.jpg")
            p.cut()
    except Exception as e:
        logger.error(e);


'''    
def wallpad( actionType, pushdata):


    t1=threading.Thread(target=_wallpad, args=[actionType,pushdata])
    t1.start()

def _wallpad(actionType,pushdata):
    pass
'''

'''
curl -X POST --header 'Content-Type: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I' -d '{
  "yid": 10000,
  "jumper": 1,
  "serial": 1
}' 'http://192.168.1.10:8000/v1/OpenToAdmin/10000'

curl -X get --header 'Host:applebox-10000.apple-box.kr' 'http://smart.apple-box.kr/v1/Rfid/kdjf'

curl -X GET --header 'Content-Type: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I'  'http://localhost:3000/v1/Order/adf'
curl -X GET --header 'Content-Type: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I'  'http://localhost:8000/v1/Notice'

curl -X PUT --header 'Content-Type: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I'  'http://smart.apple-box.kr/v2/ThingsTemp/aaaa'

'''

def OpenToAdmin(request, yid):
    logger.info('OpenToAdmin', request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.body:
        req = json.loads(request.body.decode("utf-8"))
    else:
        req = {}



    #lockerInfo = Locker.objects.get(yid=req['yid'], jumper=req['jumper'], serial=req['serial'])


    if LockerService.openDoor(req['jumper'], req['serial'], getDeviceName(req['jumper'])):

        if req.get('status')=='X':
            cv = Property.objects.filter(name='controller_version').first()

            if cv and cv.value == '2':
                LockerService.openDoor(req['jumper']+1, req['serial'] , getDeviceName(req['jumper']))
            else:
                LockerService.openDoor(req['jumper'] , req['serial']+1, getDeviceName(req['jumper']))

        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'errorCode': 500, 'message': '에러입니다.\n 다시한번 입력해주세요.'},status=500)

## 디바이스
def getDeviceName(jumper):
    if jumper<=36:
        return '/dev/hunes'
    if jumper>36 and jumper<=61:
        return '/dev/hunes2'
    if jumper>61:
        return 'dev/hunes3'
def Reserve(request,yid,status):
    logger.info('Reserve', request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!', 'errorCode': 405}, status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.body:
        req = json.loads(request.body.decode("utf-8"))
    else:
        req = []

    if status!='F' and status!='G' and status!='B':
        return JsonResponse({'success': False, 'errorCode': 405, 'message': '사용할수 없음'}, status=405)

    for locker in req:
        item = Locker.objects.filter(row=locker['row'], col=locker['col']).first()
        if item:
            if status=='F': #예약중
                if item.status!='B':
                    return JsonResponse({'success': False, 'errorCode': 405, 'message': '사용할수 없음'}, status=405)
            elif status=='G': #예약함
                if item.status!='F':
                    return JsonResponse({'success': False, 'errorCode': 405, 'message': '사용할수 없음'}, status=405)
            elif status=='B': #상태벼경
                if item.status!='F':
                    return JsonResponse({'success': False, 'errorCode': 405, 'message': '사용할수 없음'}, status=405)
        else:
            return JsonResponse({'success': False, 'errorCode': 404, 'message': 'no box'}, status=404)
    for locker in req:
        item = Locker.objects.get(row=locker['row'], col=locker['col'])

        item.status=status
        item.saveDate= iso_format(datetime.utcnow())
        item.thingsSq = locker.get("thingsSq")
        item.saveName=locker.get("saveName")
        item.usage = locker.get("usage")
        item.saveHp = locker.get("saveHp")
        item.acceptNumber=locker.get("acceptNumber");
        item.save(update_fields=['status', 'saveDate', 'saveHp', 'saveName', 'acceptNumber','thingsSq','usage'])



    return JsonResponse({'success': True})
'''
def ReserveConfirm(request,yid):
    logger.info('OpenToAll', request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!', 'errorCode': 405}, status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.body:
        req = json.loads(request.body.decode("utf-8"))
    else:
        req = []

    for locker in req:
        item = Locker.objects.get(row=locker['row'], col=locker['col'])
        if item.status!='F' and item.acceptNumber==locker['acceptNumber']:
            return JsonResponse({'success': False, 'errorCode': 405, 'message': '사용할수 없음'}, status=404)

    for locker in req:
        item = Locker.objects.get(row=locker['row'], col=locker['col'])
        if item.status=='F' and item.acceptNumber==locker['acceptNumber']:
            item.status='H'
            item.saveDate= iso_format(datetime.utcnow())
            item.saveName=locker.get("saveName")
            item.saveHp = locker.get("saveHp")
            #item.acceptNumber=locker.get("acceptNumber");
            item.save(update_fields=['status', 'saveDate', 'saveHp', 'saveName'])
        else:
            return JsonResponse({'success': False, 'errorCode': 405, 'message': '사용할수 없음'}, status=404)


    return JsonResponse({'success': True})
'''
def OpenToTakeAll(request, yid,acceptNumber):  # 예약번호로 다 찾기
    logger.info('OpenToAll', request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.body:
        req = json.loads(request.body.decode("utf-8"))
    else:
        req = {}
    errors = []
    lockers= []
    try:

        applebox = Applebox.objects.filter(yid=yid).first()

        if applebox.useType=='A':
            tpwd = Property.objects.filter(name='takepwd').first();
            if tpwd.value==acceptNumber:
                lockerList = Locker.objects.filter(status='A', acceptNumber=acceptNumber)
            else:
                lockerList=[]
        else:
            lockerList = Locker.objects.filter(status='A',acceptNumber=acceptNumber)
        print(len(lockerList))
        for lockerInfo in lockerList:
            print(model_to_dict(lockerInfo))
            req['thingsSq']=lockerInfo.thingsSq
            #lockerInfo = Locker.objects.get(yid=item['yid'], jumper=item['jumper'], serial=item['serial'])
            if LockerService.openDoor(lockerInfo.jumper, lockerInfo.serial, getDeviceName(req['jumper'])):
                lockerInfo.status='B'

                lockerInfo.save(update_fields=['status'])
                pdata = model_to_dict(lockerInfo)
                pdata['regDate'] = iso_format(datetime.utcnow())
                del pdata['id']
                del pdata['step']
                if pdata.get('sensor'):
                    del pdata['sensor']
                TakeLog(**pdata).save()


                del pdata['api_key']

                lockers.append(pdata)
            else:
                errors.append('open hardware error!')


            ##return JsonResponse({'success': True})
        if len(errors)>0:
            return JsonResponse({'success': False, 'errorCode': 500, 'message': '에러입니다.\n 다시한번 입력해주세요.', errors:errors},status=500)

        else:



            if applebox.useType!='A':
                api_key = request.api_key
                req['lockers']=lockers
                pushData = {'command': '/v1/Locker/open_to_take_all', 'api_key': api_key, 'data': req}
                if lockerEvent.sendPush(pushData, True) == False:
                    lockerEvent.insertPush('1', pushData)



            return JsonResponse({'success': True})
    except Exception as e :
        logger.exception(e)
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)
def SensorStart(request, yid):

    if request.body:
        req = json.loads(request.body.decode("utf-8"))
    else:
        req = {}

    #lockerInfo = Locker.objects.get(yid=req['yid'], jumper=req['jumper'], serial=req['serial'])

    #sp = IrCheck(req['jumper'], None)
    #sp.start()

    mIrSensor.sensorStart(req['jumper'],getDeviceName(req['jumper']))

    return JsonResponse({'success': True})

def SensorStop(request, yid):

    if request.body:
        req = json.loads(request.body.decode("utf-8"))
    else:
        req = {}

    #lockerInfo = Locker.objects.get(yid=req['yid'], jumper=req['jumper'], serial=req['serial'])

    #sp = IrCheck(req['jumper'], None)
    #sp.start()

    mIrSensor.sensorStop()

    return JsonResponse({'success': True})

'''
curl -X POST --header 'Content-Type: application/json' --header 'Host: applebox-10003.apple-box.kr' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I' -d '{"checkStatus": true}' 'http://localhost:3000/v1/AppleboxAll/10003'


연결정보를 가져오기

'''

def OpenAll(request, yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    lockerList = Locker.objects.filter(kind='B').order_by('col', 'row')
    for item in lockerList:

        ret = LockerService.openDoor(item.jumper, item.serial, getDeviceName(item.jumper))
        if ret:
            continue
        else:
            print("열기 실패 ")
            continue
            # time.sleep(1)
    return JsonResponse({'success': True})

'''

select  A.*,B.name boxName,B.location
from applebox_locker A , applebox_applebox B  where A.yid = B.yid and B.status='A' and A.status = 'A'
and A.toHp='01068115228' order by A.saveDate desc;


'''
def TakeLogList(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    num_pages = request.GET.get('display')
    if num_pages == None:
        num_pages = '10'
    num_pages = int(num_pages)
    uuid = request.GET.get('uuid')
    toHp = request.GET.get('toHp')
    saveHp = request.GET.get('saveHp')
    result_list = TakeLog.objects.all().order_by('-saveDate')
    if uuid :
        result_list = result_list.filter(uuid=uuid)
    if toHp :
        result_list.filter(toHp=toHp)
    if saveHp :
        result_list.filter(saveHp=saveHp)
    total = result_list.count()
    paginator = Paginator(result_list, num_pages) # Show 25 contacts per page

    page = request.GET.get('page')
    if page== None:
        page=1

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        logger.exception('TakeLogList')
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        logger.exception('TakeLogList')
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)

    #return JsonResponse({'success': True, 'data': dictfetchall(result)})
    rs = []
    for item in result:
        rs.append(model_to_dict(item))
    return JsonResponse({'success': True, 'data': rs,'total':total})
def PushList(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    result_list = Push.objects.all().order_by('-regDate')
    rs=[]
    for item in result_list:
        jdata = json.loads(item.data)
        if jdata.get('command')=='/v1/Locker/close_to_save':
            iitem = jdata['data']
            iitem['command']='close_to_save'
            iitem['id'] = item.id
            rs.append(iitem)
        elif jdata.get('command') == '/v1/Locker/open_to_take':
            iitem = jdata['data']
            iitem['command'] = 'open_to_take'
            iitem['id']=item.id
            rs.append(iitem)
        else:
            item.delete()

        if len(rs)==4:
            break
    return JsonResponse({'success': True, 'data': rs})

def PushDelete(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    if request.method == 'DELETE':  # 입력
        # item = {'name': request.POST.get("name"), 'value': request.POST.get("value")}

        req = json.loads(request.body.decode("utf-8"))
        for item in req:
            try:
                it= Push.objects.get(pk=item)
                if it:
                    it.delete()
            except:
                pass

    return JsonResponse({})

def ServiceList(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    result_list = Service.objects.all()

    rs = []
    for item in result_list:
        rs.append(model_to_dict(item))
    return JsonResponse({'success': True, 'data': rs})

def SaveLogList(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    num_pages = request.GET.get('display')
    if num_pages== None:
        num_pages='10'
    num_pages = int(num_pages)
    uuid = request.GET.get('uuid')
    toHp = request.GET.get('toHp')
    saveHp = request.GET.get('saveHp')
    result_list = SaveLog.objects.all().order_by('-saveDate')

    if uuid:
        result_list = result_list.filter(uuid=uuid)
    if toHp:
        result_list.filter(toHp=toHp)
    if saveHp:
        result_list.filter(saveHp=saveHp)
    total = result_list.count()
    paginator = Paginator(result_list, num_pages) # Show 25 contacts per page

    page = request.GET.get('page')
    if page== None:
        page=1

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        logger.exception('SaveLogList')
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        logger.exception('SaveLogList')
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)

    #return JsonResponse({'success': True, 'data': dictfetchall(result)})
    rs = []
    for item in result:
        rs.append(model_to_dict(item))
    return JsonResponse({'success': True, 'data': rs,'total':total})


def HouseReq(request):

    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    if request.method == 'POST':  # 입력
        # item = {'name': request.POST.get("name"), 'value': request.POST.get("value")}
        req = json.loads(request.body.decode("utf-8"))
        idata = House(**req)
        try:

            idata.save(force_insert=True)
        except Exception as e:
            return JsonResponse({'success': False, 'errorCode': 505, 'message': 'error'}, status=505)
        return JsonResponse({})
    elif request.method == 'GET':  # 목록


        list = House.objects.all()
        if request.GET.get('dong'):
            list = list.filter(dong=request.GET.get('dong'))
        rs = []
        for item in list:
            rs.append(model_to_dict(item))
        return JsonResponse(rs, safe=False)
    elif request.method == 'PUT':  #
        req = json.loads(request.body.decode("utf-8"))

        #print(req)
        try:

            udata = House.objects.filter(dong=req.get('dong'),ho=req.get('ho')).first()
            #print(udata)
            udata.pwd=req.get('pwd')

            udata.save(update_fields = ['pwd'])
        except Exception as e:
            print(e);
            return JsonResponse({'success': False, 'errorCode': 505, 'message': 'error'}, status=505)
        return JsonResponse({})
    return JsonResponse({}, status=404)

def DongList(request,dong):

    #if  isLogin(request) == False:
    #    return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)



    #result = House.objects.values('dong')

    if dong=='Dong':
        result = House.objects.values('dong').order_by('dong').annotate(count=Count('dong'))
        return JsonResponse(list(result), safe=False)
    else:
        result = House.objects.filter(dong=dong).extra({'ho_uint':'CAST(ho as integer)'}).order_by('ho_uint')
        rs = []
        for item in result:
            rs.append(model_to_dict(item))
        return JsonResponse(rs,safe=False)
def HoList(request,dong):
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)



    result = House.objects.filter(dong=dong).extra({'ho_uint':'CAST(ho as integer)'}).order_by('ho_uint')
    rs = []
    for item in result:
        rs.append(model_to_dict(item))
    return JsonResponse(rs,safe=False)
def RfidList(request):

    #if globals()['yid'] != int(yid):
    #    return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    num_pages = request.GET.get('display')
    if num_pages == None:
        num_pages = '10'
    num_pages = int(num_pages)
    uuid = request.GET.get('uuid')
    toHp = request.GET.get('toHp')
    saveHp = request.GET.get('saveHp')
    result_list = Rfid.objects.all()

    total = result_list.count()
    if uuid:
        result_list = result_list.filter(uuid=uuid)
    if toHp:
        result_list.filter(toHp=toHp)
    if saveHp:
        result_list.filter(saveHp=saveHp)
    paginator = Paginator(result_list, num_pages)  # Show 25 contacts per page

    page = request.GET.get('page')
    if page == None:
        page = 1

    try:
        result = paginator.page(page)
    except PageNotAnInteger:
        logger.exception('TakeLogList')
        # If page is not an integer, deliver first page.
        result = paginator.page(1)
    except EmptyPage:
        logger.exception('TakeLogList')
        # If page is out of range (e.g. 9999), deliver last page of results.
        result = paginator.page(paginator.num_pages)

    # return JsonResponse({'success': True, 'data': dictfetchall(result)})
    rs = []
    for item in result:
        rs.append(model_to_dict(item))
    return JsonResponse({'success': True, 'data': rs, 'total':total})
def HouseSelect(request,dong,ho):
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)


    result = House.objects.filter(dong=dong,ho=ho).first()
    if result:
        return JsonResponse(model_to_dict(result))
    else:
        return JsonResponse({'success': False, 'errorCode': 404, 'message': 'error'}, status=404)



def LockerList(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if  isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    try:
        if request.method == "PUT":
            if request.body:
                req = json.loads(request.body.decode("utf-8"))
            else:
                req = {}
            item= Locker.objects.get(row=req['row'],col=req['col'])
            item.status=req['status']
            item.toHp=req['toHp']
            item.toName=req['toName']
            item.saveHp=req['saveHp']
            item.saveDate=req['saveDate']
            item.saveName=req['saveName']
            item.save(update_fields=['status','saveDate','saveHp','saveName','toHp','toName'])
            return JsonResponse({'success': True})
        else:
            query = '''
            select  A.*,B.name boxName,B.location
            from applebox_locker A , applebox_applebox B  where A.yid = B.yid and B.status='A' and A.status = 'A'
            and A.toHp=:hp
                '''

            if request.body:
                req = json.loads(request.body.decode("utf-8"))
            else:
                req = {}
            if 'topDate' in req :
                query +=' and A.saveDate > "%s"'%req['topDate']

            #print(request.user['hp'])
            with connection.cursor() as cursor:
                #cursor.execute("UPDATE bar SET foo = 1 WHERE baz = %s", [self.baz])
                cursor.execute(query,{'hp':request.user['hp']})
                #row = cursor.fetchone()
                return JsonResponse({'success': True, 'data':dictfetchall(cursor)})
    except Exception as e:
        logger.exception('LockerList')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)
    #return row
def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]
def AppleboxAll(request,yid):

    #print(globals()['yid'],yid )

    #print(type(yid))
    if isLogin(request) ==False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not installed!!!', 'errorCode': 405}, status=405)

    '''
    if request.body:
        req = json.loads(request.body.decode("utf-8"))
    else:
        req = {}
    '''


    try:
        statusList = {}

        #isStatus = req.get('checkStatus')

        if request.GET.get('checkStatus')=='true':
            isStatus =True
        else:
            isStatus = False


        if isStatus==True:
            cv = Property.objects.filter(name='controller_version').first()
            if cv and cv.value=='2':
                ds=[]
                for j in Locker.objects.raw(
                        'SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null and jumper>0'):
                    #p = LockerService.statusBoard(j.jumper)
                    ds.append(j.jumper)
                p = LockerService.statusSensors(ds)  # 상태

                for i in p:
                    closed = rs485.isOn(i, 1)
                    if closed:
                        statusList[(i[0],1)]=True
            else:
                for j in Locker.objects.raw(
                        'SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null and jumper>0'):
                    p = LockerService.statusBoard(j.jumper, getDeviceName(j.jumper))
                    if p:
                        for i in range(1, 17):
                            closed = rs485.isOn(p, i)
                            if closed:
                                statusList[(j.jumper,i)]=True
                #else:
                #    raise Exception('컨트럴러 연결 오류 !!')
        result = {}
        datas = []
        result['applebox'] = model_to_dict(Applebox.objects.filter(yid=yid).first())
        result['applebox']['addr']=json.loads(result['applebox']['addr'])
        #print(result['applebox']['yid'])
        boxes = []
        colLabel = 65
        tcol = 0
        cursor = Locker.objects.filter(yid=result['applebox']['yid'])
        for row in cursor:
            # print(row)

            #modelRow = model_to_dict(row,fields=['yid','label','col','row','jumper','serial','status','kind','width','height','saveHp','saveName','saveDate','toHp','toName','usage'])
            modelRow = model_to_dict(row, exclude=['api_key','step'])

            if isStatus == True:
                bs = statusList.get((row.jumper,row.serial))

                if not bs :
                    modelRow['status']='C' # 전기 작동 안함
            if len(boxes) == 0:
                boxes.append(modelRow)
                tcol = row.col
            else:
                if tcol != row.col :
                    datas.append({"label": str(chr(colLabel)), "box": boxes})
                    boxes = []
                    boxes.append(modelRow)
                    tcol = row.col
                    colLabel = colLabel + 1
                else:
                    boxes.append(modelRow)

        if len(boxes) > 0:
            datas.append({"label": str(chr(colLabel)), "box": boxes})
        result['cabinet'] = datas
        resp= JsonResponse({'success': True, 'data': result})
        #resp["Access-Control-Allow-Origin"] = "http://localhost"
        #resp["Access-Control-Allow-Headers"] = "Authorization"
        #resp["Access-Control-Request-Headers"]="*"
        #resp['Access-Control-Allow-Credentials'] = 'true'
        #resp['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,PATCH,OPTIONS'
        return resp;
    except Exception as e:
        logger.exception('AppleboxAll')
        return JsonResponse({'success': False, 'message': str(e),'errorCode':500},status=500)

def GetPincode(request,yid,pincode):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)

    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :

        #url = 'http://smart.apple-box.kr:3000/v1/Pincode/'+pincode
        #url = 'http://172.24.1.95:3000/v1/Pincode/' +yid+'/'+ pincode
        #url = 'http://172.24.1.95:3000/v1/Pincode/' + yid + '/' + pincode
        url = 'http://server/v1/Pincode/'+yid+'/' + pincode

        resp = requests.get(url=url,headers={'Authorization': 'Bearer ' + settings.ATOKEN})
        if resp.status_code == 200:
            data = json.loads(resp.text)
            return JsonResponse(data)
        elif resp.status_code==422: # 이미 등록된게 있다
            res = RfidSync(request, globals()['yid'])
            return HttpResponse(resp.text, status=422)

        else :
            #return Response
            #return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
            return HttpResponse(resp.text, status=resp.status_code)
    except Exception as e:
        logger.exception('GetPincode')
        return JsonResponse({'success': False, 'errorCode':600, 'message':str(e)} ,status=600)

def ResidentUpdate(request,dong,ho):

    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        req = json.loads(request.body.decode("utf-8"))

        url = 'http://server/v1/ResidentInit/' + dong+'/'+ho
        resp = requests.put(url=url, json=req,headers={'Authorization': 'Bearer ' + settings.ATOKEN})
        if resp.status_code == 200:
            Resident.objects.filter(dong=dong,ho=ho).delete()
            for item in req:
                rd = Resident(**item)
                rd.status='A'
                rd.save(force_insert=True)
        elif resp.status_code == 422:  # 이미 등록된게 있다
            #res = RfidSync(request, globals()['yid'])
            return HttpResponse(resp.text, status=422)

        else:
            # return Response
            # return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
            return HttpResponse(resp.text, status=resp.status_code)




        return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)
    except Exception as e:
        print(e)

        return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)

def GetResident(request,tagid):

    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        #myboxs = Rfid.objects.filter(tagid=tagid, status='A')[0]
        #return JsonResponse({'success': True, 'data':model_to_dict(Rfid.objects.get(tagid=tagid))})

        if request.method =='GET' :
            tdata = Resident.objects.filter(tagid=tagid,status='A').first()


            if tdata:

                llist = Locker.objects.filter(toDong=tdata.dong, toHo=tdata.ho, status='A')
                rs = []
                for item in llist:
                    rs.append(model_to_dict(item))

                return JsonResponse(rs, safe=False)
            else:

                res = ResidentSync(request, globals()['yid'])
                if res.status_code == 500:
                    return res
                try:
                    tdata = Resident.objects.filter(tagid=tagid, status='A').first()
                    if tdata:
                        llist = Locker.objects.filter(toDong=tdata.dong, toHo=tdata.ho, status='A')
                        rs = []
                        for item in llist:
                            rs.append(model_to_dict(item))

                        return JsonResponse(rs, safe=False)
                    else:

                        return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)
                except:
                    return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)
        else:

            return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)
    except Exception as e:
        print(e)

        return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)

def GetRfid(request,tagid):
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        #myboxs = Rfid.objects.filter(tagid=tagid, status='A')[0]
        #return JsonResponse({'success': True, 'data':model_to_dict(Rfid.objects.get(tagid=tagid))})

        if request.method =='GET' :
            tdata = Rfid.objects.get(tagid=tagid)
            if tdata.status=='A':
                return JsonResponse( model_to_dict(tdata))
            else:

                return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)
        elif request.method=='PUT':
            try:
                req = json.loads(request.body.decode("utf-8"))
                print(req)
                tdata = Rfid.objects.get(tagid=req['tagid'])
                tdata.name=req['name']
                tdata.modDate = iso_format(datetime.utcnow())
                tdata.save(force_update=True)
                return JsonResponse({'success': True})
            except Exception as e:
                print(e)
                return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=501)
        elif request.method == 'POST':
            try:
                req = json.loads(request.body.decode("utf-8"))
                tdata = Rfid(**req)
                tdata.modDate = iso_format(datetime.utcnow())
                tdata.regDate = iso_format(datetime.utcnow())
                tdata.save()
                return JsonResponse({'success': True})
            except Exception as e:
                print(e)
                return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=501)
        #rlist = Rfid.objects.filter(tagid=tagid, status='A')
        #if len(rlist)==1:
        #    return JsonResponse({'success': True, 'data': model_to_dict(Rfid.objects.filter(tagid=tagid, status='A')[0])})
        #else:
        #    return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)

    except:
        #logger.exception('GetRfid')
        res = RfidSync(request, globals()['yid'])
        if res.status_code==500:
            return res
        try:
            tdata = Rfid.objects.get(tagid=tagid)
            if tdata.status == 'A':
                return JsonResponse(model_to_dict(tdata))
            else:

                return JsonResponse({'success': False, 'errorCode': 404, 'message': ''}, status=404)
        except:
            return JsonResponse({'success': False, 'errorCode':404, 'message':''} ,status=404)
def SmsAuth(request,yid,hp):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        try:
            rfid = Rfid.objects.get(tagid=hp)
            return JsonResponse({'success': False, 'errorCode': 300, 'message': '이미 등록된 핸드폰'}, status=422)

        except:
            pass
        url = 'http://server/v1/authSmsDeliverer/'+hp
        resp = requests.get(url=url,headers={'Authorization': 'Bearer ' + settings.ATOKEN})
        if resp.status_code == 200:
            data = json.loads(resp.text)
            return JsonResponse(data)
        elif resp.status_code==422: # 이미 등록된게 있다
            res = RfidSync(request, globals()['yid'])
            return HttpResponse(resp.text, status=422)

        else :
            #return Response
            #return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
            return HttpResponse(resp.text, status=resp.status_code)
    except Exception as e:
        logger.exception('RfidSync')
        return JsonResponse({'success': False, 'errorCode':600, 'message':str(e)} ,status=600)

def RfidChange(request,dong,ho):
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        req = json.loads(request.body.decode("utf-8"))
        try:
            #rs = Resident.objects.filter(yid=globals()['yid'],dong=dong,ho=ho)

            #if rs:
            #    if rs.pwd==req['pwd']:

            resp = requests.post(url='http://server/v1/RfidChange/'+str(globals()['yid']) +'/'+ dong+'/'+ ho, json=req,
                                 headers={'Authorization': 'Bearer ' + settings.ATOKEN})
            print(resp.text)
            if resp.status_code == 200:

                rfids = resp.json()
                Resident.objects.filter(yid=globals()['yid'], dong=dong, ho=ho).delete()
                for item in rfids:

                    Resident(**item).save(force_insert=True)
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
                #else:
                #    return JsonResponse({'success': False, 'message': '패스워드틀림'}, status=404)
            #else:
            #    return JsonResponse({'success': False,  'message': '정보없음'}, status=404)
        except Exception as ex:

            print(ex)
            return JsonResponse({'success': False, 'message': '에러'}, status=404)
    except Exception as e:
        #logger.exception('RfidReg')
        print(e)
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)

'''
curl -X PUT --header 'Content-Type: application/json' --header 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJtZW1iZXJTcSI6MTE5LCJocCI6IjAxMDY4MTE1MjI4IiwibmFtZSI6Iu2ZjeyEseyyoCIsIm1lZGlhIjoiQSIsImlhdCI6MTQ3MDAzNTM4M30.xNh_2_caz32PZsJp98eYsl93zStOBWXUYldw3PTu09I'  -d '{"pwd":"1111","newpass":"12345"}' 'http://192.168.0.75/v1/PasswordChange/101/101'
'''
def PasswordChange(request,dong,ho):
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        req = json.loads(request.body.decode("utf-8"))
        try:
            rs = House.objects.filter(yid=globals()['yid'],dong=dong,ho=ho).first()

            if rs:
                if rs.pwd==req['pwd']:

                    resp = requests.post(url='http://server/v1/HousePwdChange/'+str(globals()['yid']) +'/'+ dong+'/'+ ho, json=req,
                                         headers={'Authorization': 'Bearer ' + settings.ATOKEN})

                    if resp.status_code == 200:

                        rs.pwd = req['newpass']
                        rs.save(update_fields=['pwd'])
                        return JsonResponse({'success': True})
                    else:
                        return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
                else:
                    return JsonResponse({'success': False, 'message': '패스워드틀림'}, status=404)
            else:
                return JsonResponse({'success': False,  'message': '정보없음'}, status=404)
        except Exception as ex:

            print(ex)
            return JsonResponse({'success': False, 'message': '에러'}, status=404)
    except Exception as e:
        #logger.exception('RfidReg')
        print(e)
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)

def RfidReg(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        req = json.loads(request.body.decode("utf-8"))
        try:
            rs = Rfid.objects.get(tagid=req['tagid'])
            return JsonResponse({'success': True,  'message': '인증성공'}, status=200)
        except Exception as ex:
            pass
        #rfid = Rfid(**req)
        #rfid.save(update_fields=['status', 'saveDate', 'api_key'])
        resp = requests.post(url='http://server/v1/Rfid/'+req['tagid'], json=req,
                            headers={'Authorization': 'Bearer ' + settings.ATOKEN})
        print(resp.text)
        if resp.status_code == 200:

            return RfidSync(request, globals()['yid'])

        else:
            return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
        JsonResponse({'success': True, 'message': '인증성공'}, status=200)
    except Exception as e:
        logger.exception('RfidReg')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)

def ResidentSync(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        with connection.cursor() as cursor:

            cursor.execute('select max(modDate) modDate from applebox_resident')
            row = cursor.fetchone()
        modDate = row[0]
        url = 'http://server/v1/Resident'
        resp = requests.get(url=url, params={'yid':yid,'modDate': modDate},
                            headers={'Authorization': 'Bearer ' + settings.ATOKEN})
        print(resp.text)
        if resp.status_code == 200:
            data = resp.json()

            for item in data:
                rfid = Resident(**item)
                try:
                    rs = Resident.objects.get(residentSq=item['residentSq'])
                    rfid.save(force_update=True)
                except:
                    rfid.save(force_insert=True)
            return JsonResponse({'success': True})
        else :
            return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
    except Exception as e:
        print(e)
        logger.exception('ResidentSync')
        return JsonResponse({'success': False, 'errorCode':500, 'message':str(e)} ,status=500)

def LockerUpdate(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        req = json.loads(request.body.decode("utf-8"))

        rs = Locker.objects.get(row=req['row'],col=req['col'])
        rs.status=req['status']
        if req.get('kind'):
            rs.kind = req['kind']
        rs.save(force_update=True)

        return JsonResponse({'success': True})

    except Exception as e:
        logger.exception('RfidSync')
        return JsonResponse({'success': False, 'errorCode':500, 'message':str(e)} ,status=500)


def RfidSync(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        with connection.cursor() as cursor:

            cursor.execute('select max(modDate) modDate from applebox_rfid')
            row = cursor.fetchone()
        modDate = row[0]
        url = 'http://server/v1/Rfid'
        params={'modDate': modDate}

        dtype = Property.objects.filter(name='deliveryType').first()
        if dtype and dtype.value=='2':
            abox=Applebox.objects.get(yid=globals()['yid'])
            params['buyerSq']=abox.buyerSq


        resp = requests.get(url=url, params=params,
                            headers={'Authorization': 'Bearer ' + settings.ATOKEN})
        #print(resp.text)
        if resp.status_code == 200:
            data = json.loads(resp.text)

            for item in data['data']:
                rfid = Rfid(**item)
                try:
                    rs = Rfid.objects.get(tagid=item['tagid'])
                    rfid.save(force_update=True)
                except:
                    rfid.save(force_insert=True)
            return JsonResponse({'success': True})
        else :
            return JsonResponse({'success': False, 'errorCode': 406, 'message': resp.text}, status=406)
    except Exception as e:
        logger.exception('RfidSync')
        return JsonResponse({'success': False, 'errorCode':500, 'message':str(e)} ,status=500)
JWTPWD = getattr(settings, "JWTPWD", None)
def getApikey(ev):
    return jwt.encode(ev, JWTPWD, algorithm='HS256').decode('utf-8')


def NoticeSync(request):
    try :
        process = subprocess.Popen(['/home/pi/.virtualenvs/o2obox/bin/python','/home/pi/Workspace/newapp/applelocker/syncdb_notice.py'], stdin=subprocess.PIPE,
                                   stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE, shell=False)
        out, err = process.communicate()

        return JsonResponse({'success': True})
    except Exception as e:

        logger.exception(e)
        return JsonResponse({'success': False, 'errorCode':500, 'message':str(e)} ,status=500)


def LockerSync(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)
    try :
        if request.method == "PUT" :
            req = json.loads(request.body.decode("utf-8"))
            print(request.body.decode("utf-8"))
            #if True : return
            apikey = getApikey({'memberSq': 0, 'hp': '', 'name': ''})
            arrays = []
            for item in req :
                row = Locker.objects.get(yid=item['yid'],jumper=item['jumper'],serial=item['serial'])
                arrays.append(model_to_dict(row))

            r = requests.put('http://server/v1/Locker', json=arrays,
                             headers={'Authorization': 'Bearer ' + apikey})

            print(r.text)
            if r.status_code == 200:
                return JsonResponse({'success': True})

            else:
                return JsonResponse({'success': False, 'errorCode': 500, 'message': ''}, status=500)
        elif request.method=="GET":

            list = Locker.objects.filter(yid=yid)
            apikey = getApikey({'memberSq': 0, 'hp': '', 'name': ''})
            arrays = []
            for row in list:
                arrays.append(model_to_dict(row))
            r = requests.put('http://server/v1/Locker', json=arrays,
                             headers={'Authorization': 'Bearer ' + apikey})
            if r.status_code == 200:
                return JsonResponse({'success': True})
            else:
                return JsonResponse({'success': False, 'errorCode': 500, 'message': ''}, status=500)

    except Exception as e:

        logger.exception(e)
        return JsonResponse({'success': False, 'errorCode':500, 'message':str(e)} ,status=500)

def error500(request):
    #type_, value, traceback = sys.exc_info()
    #print(type_,value,traceback)
    #return JsonResponse({'success': False, 'data': {}})
    #return HttpResponse('에러 입니다 .')
    return HttpResponseServerError('1111')

def StatusLocker(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    rs =[]

    try:
        for j in Locker.objects.raw(
                'SELECT distinct jumper jumper , jumper as id FROM applebox_locker where jumper is not null'):
            p = LockerService.statusBoard(j.jumper, getDeviceName(j.jumper))
            if p:
                rs.append(p)
        #print(1111)
        return JsonResponse({'success': True, 'data':p})

    except serial.serialutil.SerialException as e:
        #logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 402, 'message': 'controller connection error'}, status=402)
    except Exception as e :
        #logger.exception('Status')
        return JsonResponse({'success': False, 'errorCode': 500, 'message': str(e)}, status=500)
def StatusReverse(request,yid):
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!','errorCode':405},status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    # ssh -o -N o2obox-tunnel
    # autossh -M 0 -o ServerAliveInterval=300 -R 42422:localhost:8000 root@125.209.200.159 -p 2222

    process = subprocess.Popen("ssh -p 2222  -o ConnectTimeout=5 root@server 'curl localhost:"+yid+" -s'", stdin=subprocess.PIPE,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE, shell=True)

    # process.stdin.write(b'tmshdnxmfl\n')
    # process.stdin.flush()

    # stdout, stderr = process.communicate()
    # print(stdout)
    # print(stderr)
    #print('here')
    out = process.communicate()[0]
    print(process.returncode)
    #print('here1')
    #print(out.decode())
    return JsonResponse({'result': out.decode()})

# J: 사업자 계기 반납 , K: 사업자 계기 수령, L: 한전 보관, M: 한전 찾기


def close_to_save_all(request):
    return JsonResponse({'success': True})

def open_to_save(request): # ㅅㅏ용안함
    return JsonResponse({'success': True})

def close_to_save(request): #

    logger.info(request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!', 'errorCode': 405}, status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)

    user = request.user
    api_key = request.api_key
    print(request.body)

    req = json.loads(request.body.decode("utf-8"))

    sdata = {}
    if req['usage'] == 'F':  # 개인보관
        sdata['dest_phone'] = req['saveHp']
        sdata['send_phone'] = Property.objects.filter(name='sendphone').first().value
        sdata['msg_body'] = Property.objects.filter(name='save_noti_personal').first().value.format(boxName=req['boxName'],
                                                                                                label=req['label'],
                                                                                                pwd=req['pwd'])
        sendSms(sdata)
        try:

            to   = Property.objects.filter(name='adminemail').first().value
            if to:
                sendMail(to,sdata['msg_body'],'['+req['toHp']+']'+sdata['msg_body'])
        except Exception as e:
            logger.error(e)
    elif req['usage'] == 'J':  # 사업자 계기 반납
        sdata['dest_phone'] = Property.objects.filter(name='adminphone').first().value
        sdata['send_phone'] = Property.objects.filter(name='sendphone').first().value
        sdata['msg_body']= Property.objects.filter(name='save_noti_busi').first().value.format(boxName=req['boxName'],label=req['label'] ,saveHp=req['saveHp'])
        sendSms(sdata)
    elif req['usage'] == 'K':  # 사업자 계기 수령
        pass
    elif req['usage'] == 'L':  # 계기 보관

        sdata['dest_phone'] = req['toHp']
        sdata['send_phone'] = Property.objects.filter(name='sendphone').first().value
        sdata['msg_body'] = Property.objects.filter(name='save_noti_root').first().value.format(boxName=req['boxName'],label=req['label'] ,pwd=req['pwd'])
        sendSms(sdata)
    elif req['usage'] == 'M':  # 전력 찾기
        pass

    return JsonResponse({'success': True})

import smtplib
from email.mime.text import MIMEText

def sendMail(to,subject,content):

    smtp = smtplib.SMTP('localhost')

    msg = MIMEText(content)
    msg['Subject'] = subject
    msg['To'] = to
    smtp.sendmail(to,to, msg.as_string())

    smtp.quit()


def open_to_take(request):
    logger.info(request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!', 'errorCode': 405}, status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)

    user = request.user
    api_key = request.api_key
    print(request.body)

    req = json.loads(request.body.decode("utf-8"))

    sdata = {}
    if req['usage']=='F': #개인찾기
        try:
            to   = Property.objects.filter(name='adminemail').first().value
            if to:
                msg= Property.objects.filter(name='take_noti_personal').first().value.format(boxName=req['boxName'],
                                                                                    label=req['label'],
                                                                                    )

                sendMail(to,msg,'['+req['toHp']+']'+msg)
        except Exception as e:
            logger.error(e)
    elif req['usage'] == 'J':  # 사업자 계기 반납
        pass
    elif req['usage'] == 'K':  # 사업자 계기 찾기
        sdata['dest_phone'] = Property.objects.filter(name='adminphone').first().value
        sdata['send_phone'] = Property.objects.filter(name='sendphone').first().value
        sdata['msg_body'] = Property.objects.filter(name='take_noti_busi').first().value.format(boxName=req['boxName'],label=req['label'] ,toHp=req['toHp'])
        sendSms(sdata)
    elif req['usage'] == 'L':  # 전력 보관

        pass
    elif req['usage'] == 'M':  # 전력  찾기
        sdata['dest_phone'] = req.get('saveHp')
        sdata['send_phone'] = Property.objects.filter(name='sendphone').first().value
        sdata['msg_body'] = Property.objects.filter(name='take_noti_root').first().value.format(boxName=req['boxName'],label=req['label'])
        sendSms(sdata)
    return JsonResponse({'success': True})
def open_to_take_all(request):
    return JsonResponse({'success': True})

def close_to_take(request): ##

    return JsonResponse({'success': True})
    '''
    logger.info(request.body)
    if globals()['yid'] != int(yid):
        return JsonResponse({'success': False, 'message': 'not yid!!!', 'errorCode': 405}, status=405)
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)

    user = request.user
    api_key = request.api_key
    print(request.body)

    req = json.loads(request.body.decode("utf-8"))

    sdata={}
    if req['usage'] =='J': #사업자 계기 반납
        sdata['dest_phone']='01068115228'
        sdata['send_phone'] = Property.objects.filter(name='feedbackPhone')
    elif req['usage'] =='K': # 사업자 계기 수령
        pass
    elif req['usage'] == 'L': # 전력 보관
        pass
    elif req['usage'] == 'M': # 전력 찾기
        pass
    return JsonResponse({'success': True})
    '''


def sendSms(sendData):
    sql = '''
                INSERT INTO BIZ_MSG set msg_type=0,cmid=DATE_FORMAT(NOW(3),'%Y%m%d%H%i%S%i%f'),request_time=now(),send_time=now(),dest_phone='{dest_phone}',send_phone='{send_phone}',msg_body='{msg_body}'
                '''

    #sql = sql % (sendData['send_phone'], sendData['dest_phone'],sendData['msg_body'])
    sql = sql.format(send_phone=sendData['send_phone'],dest_phone=sendData['dest_phone'],msg_body=sendData['msg_body'])

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            database='yellowbox',
            user="yellowbox",
            passwd="dpfshdnqkrtm", connect_timeout=3)
        mycursor = mydb.cursor()

        mycursor.execute(sql)
        mydb.commit()
        mycursor.close()
        mydb.close()
    except Exception as e:
        #print(e)
        logger.error(e)
        return False

    return True


def SmsInsert(request):
    if isLogin(request) == False:
        return JsonResponse({'success': False, 'errorCode': 403, 'message': '인증데이타가 아닙니다.'}, status=403)

    user = request.user
    api_key = request.api_key
    print(request.body)

    req = json.loads(request.body.decode("utf-8"))
    sdata={}
    sdata['dest_phone'] =req['dest_phone']
    sdata['send_phone'] = Property.objects.filter(name='sendphone').first().value
    sdata['msg_body'] = req['msg_body']
    sendSms(sdata)
    return JsonResponse({'success': True})
def SmsList(request):

    #if  isLogin(request) == False:
    #    return JsonResponse({'success': False, 'errorCode': 401, 'message': '인증데이타가 아닙니다.'}, status=401)

    #print(request)
    #return JsonResponse({'success': True})

    start = int(request.GET.get('page','1'))-1

    length = int(request.GET.get('display', '10'))

    wsql = " where cmid is not null";

    if request.GET.get('dest_phone'):
        wsql += " and dest_phone='"+request.GET.get('dest_phone')+"'";

    

    try:
        mydb = mysql.connector.connect(
            host="localhost",
            database='yellowbox',
            user="yellowbox",
            passwd="dpfshdnqkrtm", connect_timeout=3)
        mycursor = mydb.cursor(dictionary=True)

        mycursor.execute("select count(*) cnt from BIZ_MSG "+wsql)
        myresult = mycursor.fetchall()

        print(myresult)
        #myresult.get('cnt')


        mycursor.execute("select  * from BIZ_MSG "+wsql+" order by request_time desc  limit "+str(start)+","+str(length))
        myresult1 = mycursor.fetchall()
        ##for x in myresult:

        return JsonResponse({
            "total": myresult[0].get('cnt'),
            "data": _lowercase_for_list(myresult1)})

        #mydb.commit()
        mycursor.close()
        mydb.close()
    except Exception as e:
        # print(e)
        #return JsonResponse({'mesage':e.get}, status=500)
        logger.error(e)
        #return False
        raise e

def _lowercase_for_list(list):
    rs=[]
    for item in list:
        rs.append(_lowercase_for_dict_keys(item))
    return rs
def _lowercase_for_dict_keys(lower_dict):
    upper_dict = {}
    for k, v in lower_dict.items():
        if isinstance(v, dict):
            v = _lowercase_for_dict_keys(v)
        upper_dict[k.lower()] = v
    return upper_dict
#url(r'^StatusLocker/(?P<yid>[0-9]+)$', views.StatusLocker, name='StatusLocker'),
#url(r'^StatusReverse/(?P<yid>[0-9]+)$', views.StatusReverse, name='StatusReverse'),
