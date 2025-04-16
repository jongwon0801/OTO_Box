#### 파일존재 확인
```less
ls -l /home/pi/Workspace/appleapp/applelocker/imp1.py

cat /home/pi/Workspace/appleapp/applelocker/imp1.py
```

```less
import os
import sys
import django
import json
import requests
import codecs
import re
import jwt

sys.path.append("../")  # settings 경로 추가
os.environ['DJANGO_SETTINGS_MODULE'] = 'appleapp.settings'

from django.forms.models import model_to_dict
from annoying.functions import get_object_or_None

def testlist():
    rs = Applebox.objects.all()
    for v in rs:
        print(v.__dict__)

def testget():
    rs = Applebox.objects.get(yid=17)
    print(rs.__dict__)

def testinsert(applebox):
    applebox.save()

def testupdate():
    ap = Applebox(yid=17, name='상암동이야 ')
    ap.save(update_fields=["name"])

def testdelete():
    Applebox.objects.get(yid=17).delete()

def getApikey(ev):
    return jwt.encode(ev, 'ilovescotchyscotch', algorithm='HS256').decode('utf-8')

def run():
    yid = int(sys.argv[1])

    Applebox.objects.all().delete()
    Locker.objects.all().delete()

    url = 'http://smart.apple-box.kr:3000/v1/AppleboxAll/' + str(yid)
    u = {'memberSq': 0, 'hp': '', 'name': ''}
    resp = requests.get(url=url, params=None, headers={'Authorization': 'Bearer ' + getApikey(u)})
    data = json.loads(resp.text)

    with codecs.open('config.json', 'w', 'utf8') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    cvalues = data['applebox']

    # 모델에 없는 필드 제거
    cvalues.pop('qrcodeFlag', None)

    cvalues['addr'] = json.dumps(cvalues['addr'])
    applebox = Applebox(**cvalues)
    applebox.save()

    list = data['cabinet']
    for item in list:
        boxes = item['box']
        for box in boxes:
            locker = Locker(**box)
            print(model_to_dict(locker))
            locker.save()

if __name__ == '__main__':
    django.setup()
    from applebox.models import Applebox, Locker, Property
    run()

```

🔍 imp1.py가 하는 일 요약

1. 서버에서 해당 yid에 대한 Applebox 데이터와 Locker 데이터 받아오기
(REST API 호출: http://smart.apple-box.kr:3000/v1/AppleboxAll/{yid})

2. 받은 JSON 데이터를 Django 모델 (Applebox, Locker)로 저장

- 기존 DB 내용은 Applebox, Locker 모두 삭제하고 초기화

- 새 데이터로 다시 삽입

3. appleapp 설정을 로드하여 Django ORM 사용


