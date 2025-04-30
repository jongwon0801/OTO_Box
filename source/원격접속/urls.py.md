```less
# /home/pi/Workspace/newapp/appleapp/urls.py

from django.conf.urls import url
from django.contrib import admin
from . import views

url(r'^logsKivy$', views.LogsKivy, name='LogsKivy'),
url(r'^logsKivy/(?P<filename>[-\w.]+)/$', views.LogsKivyFile, name='LogsKivyFile'),
url(r'^v1/', include('applebox.urls')),
```

```less
# /home/pi/Workspace/newapp/applebox/urls.py

url(r'^AutosshStart/(?P<outport>[0-9]+)/(?P<inport>\w+)$', views.AutosshStart, name='AutosshStart'),
url(r'^AutosshStop', views.AutosshStop, name='AutosshStop'),
```

#### views는 현재 디렉터리에 있는 views.py 파일을 import한 모듈

```less
from . import views
```
즉, 이 urlpatterns 리스트는 views.py 안에 정의된 함수들을 URL 경로와 연결하고 있습니다.

```less
url(r'^logsKivy$', views.LogsKivy, name='LogsKivy')
```
1. LogsKivy는 views.py 안에 정의된 함수

```less
ex) views.py

def LogsKivy(request):
    ...
```
- views.LogsKivy는 해당 함수(뷰 함수)를 가리킵니다.

2. name='LogsKivy'

- 이건 URL 패턴의 이름입니다. 나중에 템플릿이나 리디렉션에서 이 이름으로 URL을 참조할 수 있게 해줍니다.

```less
<a href="{% url 'LogsKivy' %}">로그 보기</a>
```
- 이 name은 함수명이랑 같을 수도 있고 다를 수도 있습니다. 즉, name='showLogs'라고 해도 문제 없습니다.


```less
url(r'^logsKivy$', views.LogsKivy, name='LogsKivy')
→ 사용자가 /logsKivy 주소에 접속하면, views.py 안의 LogsKivy 함수가 실행됩니다.
```

```less
views.LogsKivy: views.py 파일 안에 정의된 함수 이름입니다.

name='LogsKivy': 이 URL 패턴을 템플릿 등에서 사용할 때의 별칭입니다.
```











