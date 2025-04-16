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
    ap.save(update_fields=["name"]) #특정한 필드 갱신
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

    url = 'http://smart.apple-box.kr:3000/v1/AppleboxAll/'+str(yid)
    u = {'memberSq': 0, 'hp': '', 'name': ''}
    resp = requests.get(url=url, params=None,headers={'Authorization': 'Bearer '+getApikey(u)})
    data = json.loads(resp.text)

    with codecs.open('config.json', 'w', 'utf8') as outfile:
        json.dump(data, outfile, sort_keys=True, indent=4, ensure_ascii=False)

    cvalues = data['applebox']

    #print(cvalues)

    #print(json.dumps(cvalues['addr']))
    cvalues['addr'] = json.dumps(cvalues['addr'])
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


    #testinsert(Applebox(**cvalues))
    #print(cvalues)
    #ab = Applebox(**cvalues)
    #ab.save()
    #print(ab)
    #print(Applebox.objects.create(**cvalues))
    #ab.__dict__.update(cvalues)
    #print(ab.__dict__)
    #ab = Applebox(**cvalues)
    #ab.yid=19
    #ab.name='lsjdflsdf'
    #print(ab)

    #print(sys.getrefcount(0))
if __name__ == '__main__':
    django.setup()
    from applebox.models import Applebox,Locker,Property
    run()
```




