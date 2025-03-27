#### 기본 연산자

| 연산자 | 의미              | 영어 단어 (줄임말)   | 예제 (a=5, b=10)         | 결과  |
|--------|-------------------|----------------------|-------------------------|-------|
| `-eq`  | 같음 (`==`)        | **equal**             | `[ "$a" -eq "$b" ]`     | ❌ (False) |
| `-ne`  | 같지 않음 (`!=`)   | **not equal**         | `[ "$a" -ne "$b" ]`     | ✅ (True)  |
| `-lt`  | 작음 (`<`)         | **less than**         | `[ "$a" -lt "$b" ]`     | ✅ (True)  |
| `-le`  | 작거나 같음 (`<=`) | **less than or equal**| `[ "$a" -le "$b" ]`     | ✅ (True)  |
| `-gt`  | 큼 (`>`)           | **greater than**      | `[ "$a" -gt "$b" ]`     | ❌ (False) |
| `-ge`  | 크거나 같음 (`>=`) | **greater than or equal** | `[ "$a" -ge "$b" ]` | ❌ (False) |


설명:
```
-eq: 두 값이 같은지 비교합니다 (equal)

-ne: 두 값이 같지 않은지 비교합니다 (not equal)

-lt: 첫 번째 값이 작은지 비교합니다 (less than)

-le: 첫 번째 값이 작거나 같은지 비교합니다 (less than or equal)

-gt: 첫 번째 값이 큰지 비교합니다 (greater than)

-ge: 첫 번째 값이 크거나 같은지 비교합니다 (greater than or equal)
```
