#### sshstart.sh
```less
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
```

#### sshstop.sh
```less
#!/bin/bash

if [[ -e /tmp/reverse_ssh.pid ]]; then   # If the file do not exists, then the
    kill `cat /tmp/reverse_ssh.pid`      #+the process is not running. Useless
    rm /tmp/reverse_ssh.pid              #+trying to kill it.
else
    echo "reverse ssh is not running"
fi
```
