#### OS 버젼 확인
```less
cat /etc/os-release

hostnamectl
```

#### stretch를 최신 버전인 buster 또는 bullseye로 변경

```less
sudo sed -i 's/stretch/buster/g' /etc/apt/sources.list

이 명령은 /etc/apt/sources.list 파일에서만 stretch를 buster로 변경합니다.
이 파일은 APT 패키지 리포지토리의 주요 목록이 들어있는 파일입니다.


sudo sed -i 's/stretch/buster/g' /etc/apt/sources.list.d/*

/etc/apt/sources.list.d/ 디렉토리에 있는 모든 파일에서 stretch를 buster로 변경합니다.
이 디렉토리에는 추가적인 리포지토리 목록 파일이 저장되어 있습니다.

두 명령 모두 실행
```

#### apt 리포지토리 업데이트
```less
sudo apt update
리포지토리 목록을 최신으로 갱신

sudo apt update --fix-missing
누락된 패키지를 자동으로 처리

sudo apt upgrade
설치된 패키지들을 최신 버전으로 업그레이드

sudo apt full-upgrade
시스템 전체 업그레이드를 통해 필요한 패키지 추가 및 제거

sudo dpkg --configure -a
깨진 설치 정리하기

sudo apt-get install -f
깨진 패키지 정리
```


#### 가상환경 가이드

```less
deactivate

rm -rf ~/venvs/o2obox

sudo apt update

# 새 가상환경 만들기
python3 -m venv ~/o2obox

# 가상환경 활성화
source ~/o2obox/bin/activate
```

#### django 실행
```less
pip install --upgrade pip

pip install django

pip install markdown_deux (안됨)

pip install markdown2

/home/pi/Workspace/appleapp/appleapp/settings.py
markdown_deux를 markdown2로 대체

pip install django-cors-headers

/home/pi/Workspace/appleapp/appleapp/views.py 에서 삭제
from django.shortcuts import render_to_response

pip install PyJWT

pip install pyserial

pip install requests

pip install django-annoying

```









