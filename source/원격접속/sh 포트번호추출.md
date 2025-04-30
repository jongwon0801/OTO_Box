```less
#!/bin/sh

serverProcessKill() {
    hostname_str="$(hostname)"
    log "Extracted hostname: $hostname_str"

    # 포트 번호 추출
    yid="$(echo "$hostname_str" | cut -d'-' -f2)"
    log "Extracted port: $yid"

    # 포트 번호가 유효한지 확인
    if echo "$yid" | grep -qE '^[0-9]+$'; then
        log "Trying to kill process using port $yid on server..."
        result=$(ssh -T -p 2222 root@server '
            # lsof 명령어를 실행하여 해당 포트를 사용하는 프로세스 확인
            lsof_output=$(lsof -ti tcp:'"$yid"')
            # lsof 명령어 결과를 로그로 출력
            echo "lsof output: $lsof_output"
            if [ -n "$lsof_output" ]; then
                kill -9 $lsof_output
                echo "Killed process using port '"$yid"' (PID: $lsof_output)"
            else
                echo "No process found using port '"$yid"'"
            fi
        ' 2>&1)  # error output captured
        log "SSH result: $result"
    else
        log "Invalid port extracted from hostname."
    fi
}
```
