#!/bin/bash

log() {
    echo "$(date +'%Y-%m-%d %H:%M:%S') - $1"
}

getPort() {
    echo "11040"
}

serverProcessKill() {
    port=$(getPort)
    log "현재 포트: $port"

    pid=$(ps aux | grep "$port" | grep "ssh" | grep -v "grep" | awk '{print $2}')

    if [ -n "$pid" ]; then
        log "프로세스 $pid 종료 중..."
        kill -9 "$pid"
    else
        log "포트 $port를 사용하는 SSH 프로세스가 없습니다."
    fi
}

startSsh() {
    port=$(getPort)
    log "리버스 SSH 연결을 시작합니다..."

    serverProcessKill

    # ✅ root 사용자가 실행하도록 SSH 키 경로 변경
    ssh -i /root/.ssh/id_rsa -o StrictHostKeyChecking=no -o ConnectTimeout=10 -f -N -R 127.0.0.1:$port:localhost:22 -p 2222 root@o2obox-tunnel

    if [ $? -eq 0 ]; then
        log "리버스 SSH 연결이 성공적으로 시작되었습니다."
    else
        log "SSH 시작에 실패했습니다!"
    fi
}

getSshProcess() {
    port=$(getPort)
    pid=$(ps aux | grep "$port" | grep "ssh" | grep -v "grep" | awk '{print $2}')
    if [ -z "$pid" ]; then
        log "SSH 프로세스가 실행되지 않았습니다."
    else
        log "SSH 프로세스 PID $pid 를 찾았습니다."
    fi
}

stopSsh() {
    port=$(getPort)
    pid=$(ps aux | grep "$port" | grep "ssh" | grep -v "grep" | awk '{print $2}')
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
