#!/bin/bash

log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

# 포트 번호를 계산하는 함수
getPort() {
    port=$(( $(hostname | awk -F"-" '{print $NF}') % 65535 ))
    echo $port
}

serverProcessKill() {
    port=$(getPort)
    log "사용할 포트: $port"
    
    # 백그라운드에서 실행 중인 SSH 프로세스를 찾기
    pid=$(pgrep -f "ssh -T -o ConnectTimeout=10 -f -N -R 127.0.0.1:$port:localhost:22 -p 2222")
    
    if [ -n "$pid" ]; then
        log "프로세스 $pid 종료 중..."
        kill -9 "$pid"
    else
        log "SSH 터널 프로세스가 실행되지 않았습니다."
    fi
}

startSsh() {
    port=$(getPort)
    log "리버스 SSH 연결을 시작합니다..."
    ssh -i ~/.ssh/id_rsa -o StrictHostKeyChecking=no -o ConnectTimeout=10 -f -N -R 127.0.0.1:$port:localhost:22 -p 2222 root@o2obox-tunnel
    if [ $? -eq 0 ]; then
        log "리버스 SSH 연결이 성공적으로 시작되었습니다."
    else
        log "SSH 시작에 실패했습니다!"
    fi
}

getSshProcess() {
    port=$(getPort)
    pid=$(pgrep -f "ssh -T -o ConnectTimeout=10 -f -N -R 127.0.0.1:$port:localhost:22 -p 2222")
    if [ -z "$pid" ]; then
        log "SSH 프로세스가 실행되지 않았습니다."
    else
        log "SSH 프로세스 PID $pid 를 찾았습니다."
    fi
}

stopSsh() {
    port=$(getPort)
    pid=$(pgrep -f "ssh -T -o ConnectTimeout=10 -f -N -R 127.0.0.1:$port:localhost:22 -p 2222")
    if [ -n "$pid" ]; then
        log "SSH 프로세스 PID $pid 를 종료 중..."
        kill -15 "$pid" || kill -9 "$pid"
    else
        log "종료할 SSH 프로세스가 없습니다."
    fi
}

initIp() {
    log "네트워크 서비스를 다시 시작합니다..."
    sudo systemctl restart dhcpcd.service
}

getIp() {
    ip=$(hostname -I | awk '{print $1}')
    if [ -z "$ip" ]; then
        log "IP 주소를 찾을 수 없습니다."
        return 1
    else
        log "현재 IP 주소: $ip"
        return 0
    fi
}

startReverseSsh() {
    serverProcessKill
    startSsh
    if [ $? -eq 0 ]; then
        log "리버스 SSH 연결이 성공적으로 설정되었습니다."
    else
        log "리버스 SSH 연결 설정에 실패했습니다."
    fi
}

log "리버스 SSH 서비스 데몬 시작..."
while true; do
    getIp
    if [ $? -ne 0 ]; then
        initIp
        stopSsh
        sleep 10
    else
        getSshProcess
        if [ -z "$pid" ]; then
            startReverseSsh
            log "리버스 SSH 서비스가 시작되었습니다."
        fi
        sleep 20
    fi
done
