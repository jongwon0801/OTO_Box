#!/bin/bash
#ssh -N -vvv o2obox-ssh &
#autossh -M 0 -N o2obox-ssh
if [[ ! -e /tmp/ssh_reverse.pid ]]; then   # Check if the file already exists
    ssh -N -vvv o2obox-ssh &                   #+and if so do not run another process.
    echo $! > /tmp/ssh_reverse.pid
else
    echo -n "ERROR: The process is already running with pid "
    cat /tmp/ssh_reverse.pid
fi
