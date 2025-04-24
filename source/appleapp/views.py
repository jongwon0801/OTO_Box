# /home/pi/Workspace/newapp/appleapp/views.py  (춘의동 11013)

# -*- coding: UTF-8 -*-

from django.http import HttpResponse
#from django.shortcuts import render_to_response
from django.shortcuts import render
from django.template import RequestContext
from django.forms.models import model_to_dict
import os
from django.http import JsonResponse, HttpResponseServerError

from applebox.models import Applebox
import os
from django.http import FileResponse
from applebox.models import Locker,LockerForm,Log,LogForm,Push,Property
import requests
import json
from wifi import Cell, Scheme
from applelocker import LockerService
def LogsPush(request):
    cursor = Push.objects.all()
    response = HttpResponse(content_type="text/plain; charset=utf-8")
    for row in cursor:
        response.write(row.data)
        response.write('\n')
    return response

def LogsKivyFile(request,filename):
    return FileResponse(open('/home/pi/.kivy/logs/' + filename, 'rb'),
                        content_type="text/plain; charset=utf-8")
def LogsDjangoFile(request,filename):

    return FileResponse(open('/home/pi/Workspace/appleapp/logs/'+filename, 'rb'),content_type="text/plain; charset=utf-8")
def LogsCams(request):
    list = os.listdir('/media/usb1')

    # print(list)


    return render(request, 'log_cams_dir.html', {
        'files': list, 'path':'datepath'
    }, content_type='text/html')

def LogsCamsFile(request,filename):

    return FileResponse(open('/media/usb1/'+filename, 'rb'),content_type="text/plain; charset=utf-8")


def LogsKivy(request):
    list = os.listdir('/home/pi/.kivy/logs')

    # print(list)


    return render(request, 'log_django_list.html', {
        'files': list, 'path':'logsKivy'
    }, content_type='text/html')
def LogsDjango(request):


    list = os.listdir('/home/pi/Workspace/appleapp/logs')

    #print(list)


    return render(request, 'log_django_list.html', {
        'files': list, 'path':'logsDjango'
    }, content_type='text/html')

def whois(request):

    applebox = Applebox.objects.all().filter()[0]

    #print(applebox)
    #version= 1.0
    if applebox:
        resp = JsonResponse(model_to_dict(applebox))
        resp["Access-Control-Allow-Origin"] = "*"
        resp['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,PATCH,OPTIONS'
        return resp

    else :
        resp = JsonResponse({'msg':'not installed'}, status=500)
        resp["Access-Control-Allow-Origin"] = "*"
        resp['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,PATCH,OPTIONS'
        return resp

    #print('aaa')
    #return render_to_response('readme.html')
    #return HttpResponse("Welcome to %s:V%s")


    #https://api-ssl.bitly.com/v3/user/link_save?access_token =df784e41415537711beaca86cd54243b521f5391&longUrl=http://wikibox.kr

def index(request):

    applebox = Applebox.objects.all().filter()[0]

    #print(applebox)
    version= 3.0
    resp = HttpResponse("Welcome to %s:%s"%(applebox.name,version))

    #resp['Cache-Control'] = 'no-cache'
    #resp["Access-Control-Allow-Origin"] = "*"
    #resp['Access-Control-Allow-Methods'] = 'GET'
    return resp

    #print('aaa')
    #return render_to_response('readme.html')
    #return HttpResponse("Welcome to %s:V%s")

def api(request):
    #return HttpResponse("Welcome to %s:V%s")

    hostname = os.uname()[1]

    yid=10000
    try:
        yid = int(hostname.split('-')[1])
    except :
        pass
    return render(request, 'o2obox.yaml', {
        'hostname':hostname,
        'yid':yid,
        'version':'1.0.0'
    }, content_type='application/yaml')

def error404(request):
    #type_, value, traceback = sys.exc_info()
    #print(type_,value,traceback)
    #return JsonResponse({'success': False, 'data': {}})
    #return HttpResponse('에러 입니다 .')
    return HttpResponseServerError('1111')

def TT(request):
    hostname =  os.uname()[1]

    #host = int(os.uname()[1].split('-')[1])


    return render(request, 'opendoor.html', {
        'hostname': hostname,
    }, content_type='text/html')


def OpenDoor(request,controller):
    #hostname =  os.uname()[1]

    LockerService.openDoor(int(controller), 1)
    return JsonResponse({'success': True})

def readme(request):
    hostname =  os.uname()[1]

    #host = int(os.uname()[1].split('-')[1])


    return render(request, 'readme.html', {
        'hostname': hostname,
    }, content_type='text/html')

def test(request):
    hostname =  os.uname()[1]

    #host = int(os.uname()[1].split('-')[1])


    return render(request, 'test.html', {
        'hostname': hostname,
    }, content_type='text/html')
def setup(request):
    hostname =  os.uname()[1]

    #host = int(os.uname()[1].split('-')[1])


    return render(request, 'setup.html', {
        'hostname': hostname,
    }, content_type='text/html')
def django(request):
    hostname =  os.uname()[1]

    return render(request, 'django.html', {
        'hostname': hostname,
    }, content_type='text/html')
def newinstall(request):
    hostname =  os.uname()[1]

    return render(request, 'newinstall.html', {
        'hostname': hostname,
    }, content_type='text/html')
def raspberrypi(request):
    hostname =  os.uname()[1]

    return render(request, 'raspberrypi.html', {
        'hostname': hostname,
    }, content_type='text/html')
def scanForCells():
    # Scan using wlan0
    cells = Cell.all('wlan0')

    # Loop over the available cells
    for cell in cells:
        cell.summary = 'SSID {} / Quality {}'.format(cell.ssid, cell.quality)

        if cell.encrypted:
            enc_yes_no = '*'
        else:
            enc_yes_no = '()'

        cell.summary = cell.summary + ' / Encryption {}'.format(enc_yes_no)

        #print(cell)
    return cells


def DeviceRegister(request):
    req = json.loads(request.body.decode("utf-8"))

    req['key']['keySq'] = 1
    resp = requests.post(url='https://smart.jiipkey.com/Locker/DeviceRegister',
                         json=req)

    if resp.status_code == 200:
        p = Property.objects.filter(name='api_key').first()
        res = resp.json()
        if p:
            p.value = res.apiKey
            p.save(update_fields=['value'])
        else:
            pdata = {'name':'api_key','value':res.apiKey}
            Property(**pdata).save()
        return JsonResponse(res)

    else:
        return JsonResponse(resp.json(), status=resp.status_code)




def WifiScan(request):
    cells = Cell.all('wlan0')

    # Loop over the available cells
    list = []
    for cell in cells:
        list.append({'ssid': cell.ssid, 'quality': cell.quality})




    print(list)
    return JsonResponse(list,safe=False)
