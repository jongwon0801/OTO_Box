#### 1. /v1/AutosshStart/<port>/<sshport> 요청 처리

```less
# /home/pi/Workspace/newapp/appleapp/urls.py

url(r'^v1/', include('applebox.urls')),
```
/v1/...으로 시작하는 요청은 applebox 앱의 urls.py 로 위임된다는 뜻


#### 2. /v1/AutosshStart/<port>/<sshport> 요청 처리
```less
/home/pi/Workspace/newapp/applebox/urls.py

url(r'^AutosshStart/(?P<outport>[0-9]+)/(?P<inport>\w+)$', views.AutosshStart, name='AutosshStart'),

이 URL은 views.AutosshStart 라는 함수(혹은 메서드)로 연결됨
```

#### 3. /v1/AutosshStart/<port>/<sshport> 요청 처리
```less
/home/pi/Workspace/newapp/applebox/views.py

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
```
