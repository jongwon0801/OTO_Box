# autosshstart.sh
```less
autossh -M 0 -R $1:localhost:$2 root@125.209.200.159 -p 2222
```

# autosshstop.sh
```less
pkill -9 ssh
```

