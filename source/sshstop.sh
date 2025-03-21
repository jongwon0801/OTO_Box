
#!/bin/bash

if [[ -e /tmp/reverse_ssh.pid ]]; then   # If the file do not exists, then the
    kill `cat /tmp/reverse_ssh.pid`      #+the process is not running. Useless
    rm /tmp/reverse_ssh.pid              #+trying to kill it.
else
    echo "reverse ssh is not running"
fi
