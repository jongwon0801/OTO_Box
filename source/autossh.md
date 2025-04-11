#### 아이비힐 RPI autossh shell

```less
# autosshstart.sh
autossh -M 0 -R $1:localhost:$2 root@125.209.200.159 -p 2222

# autosshstop.sh
pkill -9 ssh
```

