# render_to_response만 제거
# /home/pi/Workspace/appleapp/appleapp/views.py

# -*- coding: UTF-8 -*-

from django.http import HttpResponse, JsonResponse, HttpResponseServerError, FileResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
import os

from applebox.models import Applebox, Locker, LockerForm, Log, LogForm, Push

def LogsPush(request):
    cursor = Push.objects.all()
    response = HttpResponse(content_type="text/plain; charset=utf-8")
    for row in cursor:
        response.write(row.data)
        response.write('\n')
    return response

def LogsKivyFile(request, filename):
    return FileResponse(open('/home/pi/.kivy/logs/' + filename, 'rb'),
                        content_type="text/plain; charset=utf-8")

def LogsDjangoFile(request, filename):
    return FileResponse(open('/home/pi/Workspace/appleapp/logs/' + filename, 'rb'),
                        content_type="text/plain; charset=utf-8")

def LogsKivy(request):
    file_list = os.listdir('/home/pi/.kivy/logs')
    return render(request, 'log_django_list.html', {
        'files': file_list, 'path': 'logsKivy'
    }, content_type='text/html')

def LogsDjango(request):
    file_list = os.listdir('/home/pi/Workspace/appleapp/logs')
    return render(request, 'log_django_list.html', {
        'files': file_list, 'path': 'logsDjango'
    }, content_type='text/html')

def whois(request):
    applebox = Applebox.objects.all().first()
    if applebox:
        resp = JsonResponse(model_to_dict(applebox))
    else:
        resp = JsonResponse({'msg': 'not installed'}, status=500)
    
    resp["Access-Control-Allow-Origin"] = "*"
    resp['Access-Control-Allow-Methods'] = 'GET,PUT,POST,DELETE,PATCH,OPTIONS'
    return resp

def index(request):
    applebox = Applebox.objects.all().first()
    version = 3.0
    return HttpResponse("Welcome to %s:%s" % (applebox.name, version))

# def api(request):
#     hostname = os.uname()[1]
#     yid = 10000
#     try:
#         yid = int(hostname.split('-')[1])
#     except:
#         pass
#     return render(request, 'o2obox.yaml', {
#         'hostname': hostname,
#         'yid': yid,
#         'version': '1.0.0'
#     }, content_type='application/yaml')

def api(request):
    hostname = os.uname()[1]
    yid = 11040
    try:
        # '-'로 분할된 두 번째 요소를 가져옴
        yid = int(hostname.split('-')[1])  
    except IndexError:  # '-'가 없을 경우 예외 처리
        pass  # 예외 발생 시 기본값 사용
    except ValueError:  # 숫자로 변환할 수 없는 경우 예외 처리
        pass  # 예외 발생 시 기본값 사용

    return render(request, 'o2obox.yaml', {
        'hostname': hostname,
        'yid': yid,
        'version': '1.0.0'
    }, content_type='application/yaml')


def error404(request):
    return HttpResponseServerError('1111')

def readme(request):
    hostname = os.uname()[1]
    return render(request, 'readme.html', {
        'hostname': hostname,
    }, content_type='text/html')

def test(request):
    hostname = os.uname()[1]
    return render(request, 'test.html', {
        'hostname': hostname,
    }, content_type='text/html')

def setup(request):
    hostname = os.uname()[1]
    return render(request, 'setup.html', {
        'hostname': hostname,
    }, content_type='text/html')

def django(request):
    hostname = os.uname()[1]
    return render(request, 'django.html', {
        'hostname': hostname,
    }, content_type='text/html')

def newinstall(request):
    hostname = os.uname()[1]
    return render(request, 'newinstall.html', {
        'hostname': hostname,
    }, content_type='text/html')

def raspberrypi(request):
    hostname = os.uname()[1]
    return render(request, 'raspberrypi.html', {
        'hostname': hostname,
    }, content_type='text/html')
