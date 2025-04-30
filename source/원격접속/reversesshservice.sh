# serverprocesskill 로직 삭제
# #!/bin/sh 자동화 셸 쓸거면 꼭 써야함

#!/bin/sh

startSsh() {
    log "trying ssh start"
    if ssh -o ConnectTimeout=10 -f -N o2obox-tunnel 2>/tmp/ssh_error.log; then
        log "success reverse ssh"
    else
        log "ssh failed: $(cat /tmp/ssh_error.log)"
    fi
}

getSshProcess() {
    pid="$(pgrep -f -x 'ssh -o ConnectTimeout=10 -f -N o2obox-tunnel')"
}

stopSsh() {
    pid="$(pgrep -f -x 'ssh -o ConnectTimeout=10 -f -N o2obox-tunnel')"
    if [ "$pid" != "" ]; then
        log "stop ssh"
        kill "$pid"
    fi
}

initIp() {
    systemctl restart dhcpcd.service
}

getIp() {
    ip="$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)"
}

log() {
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
            startSsh
            log "start ssh"
            sleep 20
        else
            sleep 20
        fi
    fi
done
