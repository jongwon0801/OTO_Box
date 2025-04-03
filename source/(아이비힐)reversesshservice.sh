# 아이비힐 lsof 없어서 ss로 대체, 호스트 인증 안함

serverProcessKill(){
    export IFS="-"
    sentence="$(hostname)"

    for word in $sentence; do
      yid="$word"
    done

    # ss 명령어를 사용하여 TCP 포트에서 프로세스 ID를 찾고 종료합니다.
    pid=$(ss -tuln | grep ":$yid" | awk '{print $6}' | cut -d',' -f2)
    
    if [ -n "$pid" ]; then
        echo "kill -9 $pid" | su - pi && ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -T -p 2222 root@server
    else
        echo "No process found for port $yid"
    fi
}

startSsh(){
    pid="$(ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -f -N o2obox-tunnel 2>&1)"
    if [ "$?" -ne 0 ]; then
        log "$pid"
    fi
}

getSshProcess(){
    pid="$(pgrep -f -x 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -f -N o2obox-tunnel')"
}

stopSsh(){
    pid="$(pgrep -f -x 'ssh -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ConnectTimeout=10 -f -N o2obox-tunnel')"
    if [ "$pid" != ""  ]; then
        log "stop ssh"
        kill "$pid"
    fi
}

initIp(){
    systemctl restart dhcpcd.service
}

startReverseSsh(){
    serverProcessKill

    if [ "$?" -eq 0 ]; then
        startSsh
        if [ "$?" -eq 0 ]; then
            log "success reverse ssh"
        else
            log "server connection error because of sshstart"
        fi
    else
        log "no server kill"
        startSsh
        if [ "$?" -eq 0 ]; then
            log "success reverse ssh"
        else
            log "server connection error because of sshstart"
        fi
    fi
}

getIp(){
    ip="$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)"
}

log(){
    echo "$1"
    echo "Time: $(date) $1" >> /home/pi/reversessh.log
}

log "start daemon"
while true; do
    getIp

    if [ "$ip" = "" ]; then
        log "no ip"
        initIp
        stopSsh
        sleep 10
    else
        getSshProcess
        if [ "$pid" = "" ]; then
            startReverseSsh
            log "start ssh"
            sleep 20
        else
            sleep 20
        fi
    fi
done
