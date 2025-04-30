# /home/pi/Workspace/newapp/applebox/views.py
# appleapp에서 applebox를 import


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


