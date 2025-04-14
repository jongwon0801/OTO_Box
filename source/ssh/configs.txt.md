

#### nano ~/.ssh/config
```less
Host o2obox-ssh
HostName      server
User          root
Port          2222
IdentityFile  /home/pi/.ssh/id_rsa
#RemoteForward  10000 localhost:8000
RemoteForward 41010  localhost:22
ServerAliveInterval 300
ServerAliveCountMax 2
ExitOnForwardFailure yes
TCPKeepAlive yes
```

#### nano /etc/ssh/sshd_config

```less
Port 22
AddressFamily any
ListenAddress 0.0.0.0
ListenAddress ::

HostKey /etc/ssh/ssh_host_rsa_key
HostKey /etc/ssh/ssh_host_ecdsa_key
HostKey /etc/ssh/ssh_host_ed25519_key

RekeyLimit default none

SyslogFacility AUTH
LogLevel INFO

LoginGraceTime 2m
PermitRootLogin prohibit-password
StrictModes yes
MaxAuthTries 6
MaxSessions 10

PubkeyAuthentication yes

AuthorizedKeysFile .ssh/authorized_keys .ssh/authorized_keys2
AuthorizedPrincipalsFile none
AuthorizedKeysCommand none
AuthorizedKeysCommandUser nobody

HostbasedAuthentication no
IgnoreUserKnownHosts no
IgnoreRhosts yes

PasswordAuthentication yes
PermitEmptyPasswords no

ChallengeResponseAuthentication no

KerberosAuthentication no
KerberosOrLocalPasswd yes
KerberosTicketCleanup yes
KerberosGetAFSToken no

GSSAPIAuthentication no
GSSAPICleanupCredentials yes
GSSAPIStrictAcceptorCheck yes
GSSAPIKeyExchange no

UsePAM yes

AllowAgentForwarding yes
AllowTcpForwarding yes
GatewayPorts no
X11Forwarding yes
X11DisplayOffset 10
X11UseLocalhost yes
PermitTTY yes
PrintMotd no
PrintLastLog yes
TCPKeepAlive yes
UseLogin no
UsePrivilegeSeparation sandbox
PermitUserEnvironment no
Compression delayed
ClientAliveInterval 0
ClientAliveCountMax 3
UseDNS no
PidFile /var/run/sshd.pid
MaxStartups 10:30:100
PermitTunnel no
ChrootDirectory none
VersionAddendum none

Banner none

AcceptEnv LANG LC_*

Subsystem sftp /usr/lib/openssh/sftp-server
```
