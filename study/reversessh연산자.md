✅ 셸에서의 || 의미

```less
command1 || command2
```
```less
이건 "command1이 실패했을 때만 command2를 실행하라" 는 뜻.

command1이 성공하면 command2는 실행되지 않고,
command1이 실패하면 command2가 실행됨
```

🔍 예시로 이해하기
```less
rm somefile.txt || echo "파일이 없어요"
```

- rm이 성공하면: 아무 일 없음

- rm이 실패하면: "파일이 없어요" 출력됨

```less
프로그래밍 언어에서 ||는 흔히 "논리적인 OR (true 또는 false)" 의미지만,
Bash 같은 셸에서는 "앞 명령이 실패하면 뒤 명령 실행" 흐름 제어용
```

⭕ 반대 개념 &&
```less
command1 && command2
```

"command1이 성공했을 때만 command2 실행"이라는 뜻


| 연산자 | 의미                          |
|--------|-------------------------------|
| `&&`   | 앞 명령이 **성공**하면 → 뒤 명령 실행 |


#### Bash 연산자: `&&`

`&&`는 **AND 연산자**로, 앞의 명령어가 **성공(종료 코드 0)** 했을 경우에만 뒤의 명령어를 실행합니다.

### 예시:
```less
mkdir new_folder && cd new_folder
```

✅ 파이프 |의 의미

```less
command1 | command2
```

```less
command1의 출력(output)을 command2의 입력(input)으로 넘겨주는 것을 의미

앞에서 나오는 결과를 바로 다음 명령어가 받아서 처리
```

🔍 코드 예시

```less
ip="$(ip -o -4 addr list eth0 | awk '{print $4}' | cut -d/ -f1)"
```

🔍 단계별 분석

✅ 1. ip -o -4 addr list eth0
```less
ip → 네트워크 설정 확인 명령

-o → one-line 형식 (인터페이스마다 한 줄로 출력)

-4 → IPv4 주소만 출력

addr list eth0 → eth0 인터페이스의 주소 목록을 보여줘
```
📌 예시 출력
```less
2: eth0    inet 192.168.0.15/24 brd 192.168.0.255 scope global eth0
```

✅ 2. awk '{print $4}'
```less
출력의 4번째 필드를 출력

위 예시에서는 192.168.0.15/24
```

📌 결과
```less
192.168.0.15/24
```

✅ 3. cut -d/ -f1
```less
/를 구분자로 나눠서 (-d/)

첫 번째 필드만 추출 (-f1)

즉, 192.168.0.15/24 → 192.168.0.15
```

📌 최종 결과
```less
192.168.0.15
```

✅ 4. ip="$( ... )"
```less
이 전체 명령의 결과를 ip 변수에 저장함

이젠 $ip 하면 192.168.0.15 가 나옴
```




















