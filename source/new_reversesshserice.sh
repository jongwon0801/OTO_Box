#!/bin/bash

# 기본 변수 정의
SSH_USER="pi"                 # SSH 사용자 이름 (pi 사용자로 변경)
REMOTE_SERVER="smart.apple-box.kr"    # 원격 서버 주소
REMOTE_PORT=22                # 리버스 SSH 포트 (로컬 포트)
TUNNEL_NAME="o2obox-tunnel"    # SSH 터널 이름

# 로그 출력 함수
log() {
    echo "$1"
    echo "Time: $(date) $1" >> /home/pi/reversessh.log
}

# 서버 프로세스 종료 함수
serverProcessKill() {
    # SSH가 실행 중인 포트를 기준으로 종료
    pid=$(lsof -ti tcp:$REMOTE_PORT)
    if [ -n "$pid" ]; then
        echo "Killing process on port $REMOTE_PORT"
        kill -9 $pid
    else
        log "No process found to kill."
    fi
}

# SSH 연결 시작 함수
startSsh() {
    # URL을 통해 서버에 요청
    curl -v -X GET --header "Host: applebox-$1.apple-box.kr" "http://smart.apple-box.kr/v1/AutosshStart/$1/22"
    
    # SSH 연결 시작
    ssh -p "$(($1+30000))" pi@localhost
    if [ "$?" -ne 0 ]; then
        log "Error starting SSH tunnel."
        return 1
    else
        log "SSH tunnel started successfully."
        return 0
    fi
}

# SSH 프로세스 확인 함수
getSshProcess() {
    pid=$(pgrep -f "ssh -o ConnectTimeout=10 -f -N -T -R $REMOTE_PORT:localhost:$LOCAL_PORT")
}

# SSH 프로세스 종료 함수
stopSsh() {
    pid=$(pgrep -f "ssh -o ConnectTimeout=10 -f -N -T -R $REMOTE_PORT:localhost:$LOCAL_PORT")
    if [ -n "$pid" ]; then
        log "Stopping SSH process with PID: $pid"
        kill "$pid"
    else
        log "No SSH process found to stop."
    fi
}

# IP 갱신 함수 (DHCP)
initIp() {
    log "IP renewal in progress."
    systemctl restart dhcpcd.service
}

# 리버스 SSH 터널 시작 함수
startReverseSsh() {
    serverProcessKill
    if [ "$?" -eq 0 ]; then
        startSsh "$1"
        if [ "$?" -eq 0 ]; then
            log "Successfully established reverse SSH tunnel."
        else
            log "Failed to establish SSH tunnel."
        fi
    else
        log "No server process to kill."
        startSsh "$1"
        if [ "$?" -eq 0 ]; then
            log "Successfully established reverse SSH tunnel."
        else
            log "Failed to establish SSH tunnel."
        fi
    fi
}

# IP 주소 가져오는 함수
getIp() {
    ip=$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)
}

# 서비스 로그 시작
log "Starting Reverse SSH Tunnel Daemon"

# 무한 루프
while true; do
    getIp

    if [ -z "$ip" ]; then
        log "No IP address found, restarting DHCP client."
        initIp
        stopSsh
        sleep 10
    else
        getSshProcess
        if [ -z "$pid" ]; then
            startReverseSsh "$1"   # $1을 전달하여 startReverseSsh를 호출
            log "Attempting to start SSH tunnel."
            sleep 20
        else
            log "SSH tunnel already established, no action needed."
            sleep 20
        fi
    fi
done
