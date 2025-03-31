# 서머셋펠리스 reversesshservice.sh

#!/bin/bash

serverProcessKill(){
    pid=$(pgrep -f -x "ssh -o ConnectTimeout=10 -f -N o2obox-tunnel")
    if [ ! -z "$pid" ]; then
        echo "Killing process $pid"
        sudo kill -9 "$pid"
    else
        echo "No process found for ssh tunnel"
    fi
}


startSsh(){
    pid="$(ssh -o ConnectTimeout=10 -f -N o2obox-tunnel 2>&1)"
    if [ "$?" -ne 0 ]; then
            log "$pid"
    fi
}
getSshProcess(){
    pid="$(pgrep -f -x 'ssh -o ConnectTimeout=10 -f -N o2obox-tunnel')"

}
stopSsh(){
    pid="$(pgrep -f -x 'ssh -o ConnectTimeout=10 -f -N o2obox-tunnel')"
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
            log "server connection error becauseof sshstart";

        fi
    else
       log "no server kill";

        startSsh
        if [ "$?" -eq 0 ]; then
            log "success reverse ssh"
        else
            log "server connection error becauseof sshstart";

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
while true;do

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
