#### AutosshStart 수정코드

```less
from django.http import JsonResponse
import subprocess

def AutosshStart(request, outport, inport):
    # 문자열로 변환 필수!
    command = ['/home/pi/reversessh.sh', 'start', str(outport), str(inport)]

    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print(stdout.decode())
    if stderr:
        print("ERROR:", stderr.decode())

    return JsonResponse({'success': True})


def AutosshStop(request):
    command = ['/home/pi/reversessh.sh', 'stop']
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = process.communicate()

    print(stdout.decode())
    if stderr:
        print("ERROR:", stderr.decode())

    return JsonResponse({'success': True})

```

#### 에러 원인

✅ 1. shell=True와 리스트 인자의 충돌 제거

🚫 이전 코드
```less
subprocess.Popen([...], shell=True)  # 인자는 리스트인데 shell=True임
```

- shell=True는 문자열 명령어일 때 사용해야 합니다.

- 리스트로 명령을 줄 경우에는 shell=False가 맞습니다.

- shell=True와 리스트를 함께 쓰면 내부적으로 문제가 생겨 스크립트가 실행되지 않거나, 인자가 잘 전달되지 않을 수 있습니다.


✅ 지금 코드 (shell=False (기본값) -> shell=False는 명시할 필요 없이 기본값으로 잘 동작)
```less
subprocess.Popen([...], shell=False)  # 올바른 방식
```
- shell=False일 때 리스트 인자 사용 → subprocess가 정확하게 실행됩니다.


✅ 2. outport, inport를 문자열로 변환함

🚫 이전 코드

```less
['/home/pi/reversessh.sh', 'start', outport, inport]  # 정수형 인자가 포함될 가능성 있음
```

- Python subprocess는 리스트 안에 정수 타입이 들어가면 예외 발생할 수 있습니다.

✅ 지금 코드
```less
['/home/pi/reversessh.sh', 'start', str(outport), str(inport)]
```
- 문자열로 명확히 변환 → 안전하게 전달됨.


✅ 3. process.communicate() 호출로 출력 캡처 및 오류 확인

🚫 이전 코드

- communicate() 없이 프로세스를 그냥 실행 → 에러가 발생해도 사용자나 개발자가 인지할 수 없음.

✅ 지금 코드
```less
stdout, stderr = process.communicate()
print(stdout.decode())
if stderr:
    print("ERROR:", stderr.decode())
```

- 실제 SSH 연결이 실패했는지, PID 파일이 이미 존재해서 중복 실행됐는지 등 실행 결과를 확인할 수 있게 됨.

📌 결론
```less
subprocess 사용 시 shell=False, 문자열 인자 전달, 그리고 출력 확인
```









