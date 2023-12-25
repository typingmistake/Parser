# PL_Project1
PL_Project1 - Parser

## Build and Test Environment
- OS : Windows 10
- Python3

## How to Run
```bash
python3 .\main.py .\text.txt
```
or
```bash
java -jar .\main.py -v .\text.txt
```


## Exception Handling
### Error
1. 선언되지 않은 `IDENT` 사용
2. 해당되는 `Token`이 없는 경우
3. `IDENT`가 두 개 이상 입력된 경우
4. 괄호의 짝이 맞지 않는 경우
5. `Term`이 존재하지 않는 경우
6. `Factor`가 존재하지 않는 경우
7. `0`으로 나눠지는 경우 (zero - division)


### Warning
1. `+`, `-`덧셈 연산자가 연속해서 나오는 경우 두번째 연산자부터 무시
2. `*`, `/` 곱셈 연산자가 연속해서 나오는 경우 두번째 연산자부터 무시
3. `:=` 할당 연산자가 연속해서 나오는 경우 두번째 연산자부터 무시


## Parser_typeA
### 목적
Parser_typeA는 식별자, 상수, 할당 연산자, 산술 연산자, 괄호를 포함하는 간단한 산술 표현식을 파싱하고 계산하는 데 사용됩니다. 이 클래스는 표현식의 구문적 정확성을 검증하고, 계산 결과를 제공합니다.

### 주요 메서드
parse_program(): 파싱을 시작하는 메서드입니다. parse_statements()를 호출하여 표현식을 처리하고 결과를 출력합니다.
parse_statements(): 여러 개의 문장을 파싱합니다. 전체문장을 lex()를 호출하여 토큰화하고,세미콜론으로 구분된 토큰을 넘깁니다.
parse_statement(): 개별 문장을 파싱합니다. 할당 연산자와 표현식을 처리합니다.
parse_expression(): 산술 표현식을 파싱합니다. 덧셈과 뺄셈 연산을 처리합니다.
parse_term(): 곱셈과 나눗셈 연산을 처리합니다.
parse_factor(): 식별자, 상수, 괄호가 포함된 표현식을 파싱합니다.

### 추가 기능
에러 및 경고 메시지: 구문 오류 또는 경고가 발생하면 적절한 메시지를 출력합니다.# Parser
