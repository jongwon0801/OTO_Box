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

def AutosshStart(request, outport, inport):
    process = subprocess.Popen(
        ['/home/pi/reversessh.sh', "start", outport, inport],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=False
    )
    return JsonResponse({'success': True})

def AutosshStop(request):
    process = subprocess.Popen(['sh', '/home/pi/reversessh.sh', 'stop'])
    return JsonResponse({'success': True})
```

```less
#!/bin/bash
NAME=reversessh
DESC="reversessh to server"
case "$1" in
  start)
    echo -n "Starting $DESC: "
    echo "$NAME."
    if [ ! -e /tmp/reverse_ssh.pid ]; then   # Check if the file already exists
        #ssh -f -N -T -R40000:localhost:22 root@smart.zimcarry.net -p 2222&
        ssh -N o2obox-ssh&
        echo $! > /tmp/reverse_ssh.pid
    else
        echo -n "ERROR: The process is already running with pid "
        cat /tmp/reverse_ssh.pid
        kill `cat /tmp/reverse_ssh.pid`      #+the process is not running. Useless
        rm /tmp/reverse_ssh.pid
        ssh -N o2obox-ssh&
        echo $! > /tmp/reverse_ssh.pid
    fi

    ;;
  stop)
    echo -n "Stopping $DESC: "
    if [ -f /tmp/reverse_ssh.pid ]; then   # If the file do not exists, then the
        kill `cat /tmp/reverse_ssh.pid`      #+the process is not running. Useless
        rm /tmp/reverse_ssh.pid              #+trying to kill it.
    else
        echo "reverse ssh is not running"
    fi
    ;;
  restart)
    $0 stop
    sleep 1

    $0 start
    ;;
  *)
    echo "Usage: $0 {start|stop|restart}" >&2
    exit 1
    ;;

esac

exit 0
```
