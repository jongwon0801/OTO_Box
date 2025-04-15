#!/bin/bash

# 로그 함수
log(){
    echo "$1"
    echo "Time: $(date) $1" >> /home/pi/reversessh.log
}

# SSH 프로세스 확인 함수 (포트별로 따로 확인)
# 같은 pid 로 연결됨
getSshProcess11040(){
    pid11040="$(pgrep -f 'ssh .*11040:localhost:22.*root@o2obox-tunnel')"
}

getSshProcess41040(){
    pid41040="$(pgrep -f 'ssh .*41040:localhost:22.*root@o2obox-tunnel')"
}

# SSH 연결 종료 함수 (전체 중단 원할 때 사용)
stopSsh(){
    pids="$(pgrep -f 'ssh .*root@o2obox-tunnel')"
    if [ "$pids" != "" ]; then
        log "Stopping all SSH tunnels (PIDs: $pids)"
        kill $pids
    fi
}

# IP 초기화 함수
initIp(){
    systemctl restart dhcpcd.service
}

# Reverse SSH 연결 시작 함수 (포트별 분리)
# 같은 SSH 프로세스에서 두 포트를 처리
startReverseSsh11040(){
    ssh -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -f -N -R 11040:localhost:22 \
        -p 2222 root@o2obox-tunnel
    if [ "$?" -eq 0 ]; then
        log "Started reverse SSH on port 11040"
    else
        log "Failed to start reverse SSH on port 11040"
    fi
}

startReverseSsh41040(){
    ssh -o StrictHostKeyChecking=no \
        -o UserKnownHostsFile=/dev/null \
        -f -N -R 41040:localhost:22 \
        -p 2222 root@o2obox-tunnel
    if [ "$?" -eq 0 ]; then
        log "Started reverse SSH on port 41040"
    else
        log "Failed to start reverse SSH on port 41040"
    fi
}

# IP 확인 함수
getIp(){
    ip="$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)"
}

# 데몬 시작
log "Starting Reverse SSH Daemon"

# 포트별로 3번 시도하는 변수 (max_attempts=3으로 변경)
attempts11040=0
attempts41040=0
max_attempts=3

while true; do
    getIp

    if [ "$ip" = "" ]; then
        log "No IP address found, restarting network"
        initIp
        stopSsh
        attempts11040=0  # IP 재시도 후 시도 횟수 리셋
        attempts41040=0
        sleep 10
    else
        getSshProcess11040
        getSshProcess41040

        # 포트 11040 - 3번은 무조건 시도
        if [ "$attempts11040" -lt "$max_attempts" ]; then
            log "Starting reverse SSH on port 11040 (Attempt #$((attempts11040+1)))"
            startReverseSsh11040
            attempts11040=$((attempts11040 + 1))
        fi

        # 포트 41040 - 3번은 무조건 시도
        if [ "$attempts41040" -lt "$max_attempts" ]; then
            log "Starting reverse SSH on port 41040 (Attempt #$((attempts41040+1)))"
            startReverseSsh41040
            attempts41040=$((attempts41040 + 1))
        fi

        # 3번 시도 이후에만 프로세스 확인해서 중단
        if [ "$attempts11040" -ge "$max_attempts" ] || [ -n "$pid11040" ] || [ -n "$pid41040" ]; then
            if [ -n "$pid11040" ] || [ -n "$pid41040" ]; then
                log "SSH tunnel already running for either port 11040 or 41040 (PID11040: $pid11040, PID41040: $pid41040), skipping further attempts"
                attempts11040=$((max_attempts + 1000))  # 더 이상 시도하지 않도록 설정
                attempts41040=$((max_attempts + 1000))  # 더 이상 시도하지 않도록 설정
            fi
        else
            # 프로세스가 없으면 3번 시도 후 다시 시도
            if [ "$attempts11040" -ge "$max_attempts" ]; then
                log "No SSH tunnel running for port 11040, retrying..."
                attempts11040=0  # 프로세스가 없으면 시도 횟수 리셋
            fi

            if [ "$attempts41040" -ge "$max_attempts" ]; then
                log "No SSH tunnel running for port 41040, retrying..."
                attempts41040=0  # 프로세스가 없으면 시도 횟수 리셋
            fi
        fi

        sleep 20
    fi
done
