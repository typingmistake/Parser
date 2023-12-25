import re

TOKEN_TYPES = {
    'IDENTIFIER': r'[a-zA-Z_][a-zA-Z_0-9]*',
    'CONSTANT': r'\d+',
    'ASSIGN_OP': r':=',
    'SEMI_COLON': r';',
    'ADD_OP': r'\+|-',
    'MULT_OP': r'\*|/',
    'LEFT_PAREN': r'\(',
    'RIGHT_PAREN': r'\)',
}

# 토큰 class : type, value를 문자열로 저장
class Token:
    def __init__(self, type, value):
        self.type = str(type)
        self.value = str(value)

    def __str__(self):
        return f"{self.type}"

    def __repr__(self):
        return self.__str__()

# 재귀 하향 파서
class Parser_typeA:
    def __init__(self, statements):
        
        # parsing 대상 statements
        self.statements = statements
        self.tokens = []
        self.current_token = None
        self.currrent_position = 0
        
        self.Warning_flag = 0
        self.Error_flag = 0
        self.message = ""
        
        self.count_id = 0
        self.count_const = 0
        self.count_op = 0
        
        # key : identifier ; value : value
        self.identifiers = {}

    def next_token(self):
        if self.tokens:
            self.current_token = self.tokens.pop(0)
        else:
            self.current_token = None  # 토큰이 더 이상 없을 때
        
    # lexical analizer : Token을 반환
    def lex(self):

        while self.currrent_position < len(self.statements):
            match = None
            
            for token_type, token_regex in TOKEN_TYPES.items():
                regex = re.compile(token_regex)
                match = regex.match(self.statements, self.currrent_position)
                
                if match:
                    value = match.group(0)
                    self.currrent_position = match.end()
                    return Token(token_type,value)
                
            if not match:
                # 공백, 줄바꿈, 탭은 건너뛴다
                if re.match(r'\s', self.statements[self.currrent_position]):
                    self.currrent_position += 1
                # 예외처리 - 해당하는 token이 없을 때
                else:
                    self.Error_flag = 1
                    self.currrent_position += 1
                    return Token("Unknown", self.statements[self.currrent_position-1])
        # 토큰이 없다면 None을 리턴
        return None
    
    # 결론 PRINT
    def parse_program(self):
        print(self.parse_statements())
    
    # STATEMENTS
    def parse_statements(self):
        self.current_token = self.lex()
        statements = []
        
        while self.current_token is not None:
            statement = []
            
            while self.current_token is not None and self.current_token.type != 'SEMI_COLON':
                statement.append(self.current_token)
                self.current_token = self.lex()
            
            statements.append([statement,self.Error_flag])
            self.Error_flag = 0
                
            if self.current_token is not None and self.current_token.type == 'SEMI_COLON':
                self.current_token = self.lex()
                
        for statement in statements:
            if statement[1]==0:
                self.parse_statement(statement[0])
            else:
                print(f"{' '.join([token.value for token in statement[0]])}")
                print("(Error)" + "Unknown Token이 입력됨.")

        return self.identifiers
    
    # STATEMENT
    def parse_statement(self,statement):
        # flag 초기화
        self.Warning_flag = 0
        self.Error_flag = 0
        value = 0
        
        #토큰 초기화
        self.tokens = statement.copy()
        self.current_token = None
        self.next_token()
        
        # count 초기화
        self.count_id = 0
        self.count_const = 0
        self.count_op = 0
        
        ident = []
        assign_op = []
        expression = []
        
        # IDENT 저장
        while self.current_token is not None and self.current_token.type != 'ASSIGN_OP':
            ident.append(self.current_token)
            self.next_token()
        
        # ASSIGN_OP 저장
        while self.current_token is not None and self.current_token.type == 'ASSIGN_OP':
            assign_op.append(self.current_token)
            self.next_token()
        
        # EXPRESSION 저장
        while self.current_token is not None:
            expression.append(self.current_token)
            self.next_token()

        if len(ident)==1:        
        # ient가 수가 1인 경우 정상 실행
            self.count_id+=1
            identifier = ident[0].value
            
        # 예외처리 - ident의 수가 1이 아닐 때
        else:
            self.Error_flag = 1
            print(f"{' '.join([token.value for token in statement])}")
            print("(Error)" + "identifier 에러")
            return None
        
        # assign_op의 수가 1인 경우 정상 실행
        if len(assign_op)==1:
            self.count_op+=1
        # 예외처리 - assign_op의 수가 1이 아닌 경우
        else:
            # warning 발생 : assign_op를 하나로 감소시켜서 해결
            if assign_op:
                self.Warning_flag = 1
                self.message = "(Warning)" + "중복 연산자(:=) 제거"
                self.count_op+=1
        
        # expression이 존재하는 경우 정상 실행
        if expression:
            value = self.parse_expression(expression)
        # 예외처리 - expression이 존재하지 않는 경우
        else:
            print(f"{' '.join([token.value for token in statement])}")
            print("(Error)" + "expression 에러")
            return None
        
        # 문장 별 출력 부분
        if self.Error_flag == 1:
            print(f"{' '.join([token.value for token in statement])}")
            print("(Error)"+self.message)
        elif self.Warning_flag == 1 :
            print(
                f"{' '.join([token.value for token in statement])}\n",
                f"ID: {self.count_id};",
                f"CONST: {self.count_const};",
                f"OP: {self.count_op};"
            )
            print("(Warning)"+self.message)
            self.identifiers[identifier]=value
        else :
            print(
                f"{' '.join([token.value for token in statement])}\n",
                f"ID: {self.count_id};",
                f"CONST: {self.count_const};",
                f"OP: {self.count_op};"
            )
            print("(OK)")
            self.identifiers[identifier]=value
    
    # EXPRESSION
    def parse_expression(self,expression):
        #토큰 초기화
        self.tokens = expression
        self.current_token = None
        self.next_token()
        value = 0
        
        term = []
        term_tail = []
        left_paren = []
        right_paren = []
        
        # term
        while self.current_token is not None :
            if self.current_token.type == 'ADD_OP' and len(left_paren) == len(right_paren):
                break
            else:  
                if self.current_token.type == 'LEFT_PAREN' :
                    left_paren.append(self.current_token)
                elif self.current_token.type == 'RIGHT_PAREN' :
                    right_paren.append(self.current_token)
                
                term.append(self.current_token)
                self.next_token()
            
        # term_tail
        while self.current_token is not None:
            term_tail.append(self.current_token)
            self.next_token()
        
        # 예외처리 - 괄호 개수가 맞지 않는 경우
        if len(left_paren) != len(right_paren):
            self.Error_flag = 1
            self.message = "괄호의 개수가 맞지 않습니다."
        
        if term:
            value+=self.parse_term(term)
        # 예외처리 - term이 존재하지 않는 경우
        else:
            self.Error_flag = 1
            self.message = "Term이 존재하지 않습니다."
        
        # term_tail이 존재하는 경우
        if term_tail:
            value+=self.parse_term_tail(term_tail)
        
        return value
    
    # TERM
    def parse_term(self, term):
        #토큰 초기화
        self.tokens = term
        self.current_token = None
        self.next_token()
        
        factor = []
        factor_tail = []
        left_paren=[]
        right_paren=[]
        value = 0
        
        while self.current_token is not None :
            if self.current_token.type == 'MULT_OP' and len(left_paren) == len(right_paren):
                break
            else:  
                if self.current_token.type == 'LEFT_PAREN' :
                    left_paren.append(self.current_token)
                elif self.current_token.type == 'RIGHT_PAREN' :
                    right_paren.append(self.current_token)
                
                factor.append(self.current_token)
                self.next_token()
        
        
        while self.current_token is not None:
            factor_tail.append(self.current_token)
            self.next_token()
            
        # 예외처리 - 괄호 개수가 맞지 않는 경우
        if len(left_paren) != len(right_paren):
            self.Error_flag = 1
            self.message = "괄호의 개수가 맞지 않음."
        
        # factor가 1개 이상 있는 경우
        if factor:
            value=self.parse_factor(factor)
        # 예외처리 - factor가 없는 경우
        else:
            self.Error_flag = 1
            self.message = "Factor가 존재하지 않음."
        
        # factor_tail이 있는 경우
        if factor_tail:
            value*=self.parse_factor_tail(factor_tail)
        
        return value
    
    # TERM_TAIL
    def parse_term_tail(self, term_tail):
        #토큰 초기화
        self.tokens = term_tail
        self.current_token = None
        self.next_token()
        
        add_op = []
        term = []
        term_tail = []
        value = 0
        
        while self.current_token is not None and self.current_token.type == 'ADD_OP':
            add_op.append(self.current_token)
            self.next_token()
        
        while self.current_token is not None and self.current_token.type != 'ADD_OP':
            term.append(self.current_token)
            self.next_token()
        
        while self.current_token is not None:
            term_tail.append(self.current_token)
            self.next_token()
        
        if len(add_op)==1:
            self.count_op+=1
        # 예외처리 - '+'가 하나가 아닌 경우
        else:
            self.Warning_flag = 1
            self.message = "중복 연산자(+/-) 제거"
            self.count_op+=1
        
        if term:
            if add_op[0].value == '+':
                value+=self.parse_term(term)
            else :
                value-=self.parse_term(term)
        # 예외처리 - term이 없는 경우
        else:
            self.Error_flag = 1
            self.message = "Term이 존재하지 않음."
        
        if term_tail:
            value+=self.parse_term_tail(term_tail)
        
        return value
    
    # FACTOR_TAIL
    def parse_factor_tail(self, factor_tail):
        # 토큰 초기화
        self.tokens = factor_tail
        self.current_token = None
        self.next_token()
        
        mult_op = []
        factor = []
        factor_tail = []
        value = 1
        count_parenthesis = 0
        
        # 현재 토큰이 곱셈 또는 나눗셈 연산자인 경우
        while self.current_token is not None and self.current_token.type == 'MULT_OP':
            mult_op.append(self.current_token)
            self.next_token()

        # 다음 factor 계산
        while self.current_token is not None:
            if self.current_token.type == 'RIGHT_PAREN':
                count_parenthesis-=1
            elif self.current_token.type == 'LEFT_PAREN':
                count_parenthesis+=1 
                
            if self.current_token.type == 'MULT_OP' and count_parenthesis == 0:
                break
            factor.append(self.current_token)
            self.next_token()
        
        if count_parenthesis != 0 :
            self.Error_flag = 1
            self.message = "Mismatched 괄호"
            
        while self.current_token is not None :
            factor_tail.append(self.current_token)
            self.next_token()
        
        if len(mult_op) == 1:
            self.count_op+=1
            operator = mult_op[0].value
        # 예외처리 - mult_op가 2개 이상인 경우
        else:
            self.Warning_flag = 1
            self.message = "중복 연산자(*)또는(/) 제거"
            self.count_op+=1
            operator = mult_op[0].value
        
        # factor 처리
        if factor:
            factor_value = self.parse_factor(factor)
            
            # 연산자에 따라 계산
            if operator == '*':
                value *= factor_value
            elif operator == '/':
                if factor_value != 0:
                    value /= factor_value
                # 예외처리 - 0으로 나눠지는 경우
                else:
                    self.Error_flag = 1
                    self.message="zero-Division 에러"
        else:
            # 예외처리 - factor가 없는 경우 
            self.Error_flag = 1
            self.message = "Factor가 존재하지 않음"
        
        if factor_tail:
            value *= self.parse_factor_tail(factor_tail)
            
        return value
    
    # FACTOR
    def parse_factor(self, factor):
        #토큰 초기화
        self.tokens = factor.copy()
        self.current_token = None
        self.next_token()
        value = 0
        count_parenthesis = 0

        # 현재 토큰이 식별자인 경우
        if self.current_token is not None and self.current_token.type == 'IDENTIFIER':
            ident = []

            while self.current_token != None:
                ident.append(self.current_token)
                self.next_token()

            if len(ident)==1:
                self.count_id+=1
                if ident[0].value in self.identifiers:
                    value = int(self.identifiers[ident[0].value])
                else:
                    self.Error_flag = 1
                    self.message = "정의되지 않은 변수 ("+ident[0].value+") 참조"
            else:
                self.Error_flag = 1
                self.message = "identifier error"

        # 현재 토큰이 상수인 경우
        elif self.current_token is not None and self.current_token.type == 'CONSTANT':
            constant = []

            while self.current_token != None:
                constant.append(self.current_token)
                self.next_token()

            if len(constant) == 1:
                self.count_const+=1
                value = int(constant[0].value)

        # 현재 토큰이 '(' 인 경우 (괄호 처리)
        elif self.current_token is not None and self.current_token.type == 'LEFT_PAREN':
            self.next_token()
            expression = []
            count_parenthesis+=1

            # ')'의 수가 채워질 때까지 토큰 수집
            while self.current_token is not None:
                if self.current_token.type == 'RIGHT_PAREN':
                    count_parenthesis-=1
                    if count_parenthesis == 0:
                        break
                elif self.current_token.type == 'LEFT_PAREN':
                    count_parenthesis+=1
                    
                expression.append(self.current_token)
                self.next_token()
                
            if count_parenthesis == 0:
                value = self.parse_expression(expression)  # 괄호 안의 표현식 파싱
            else:
                self.Error_flag = 1
                self.message = "Mismatched 괄호"

        return value

def ParsingStatements(code):
    parser = Parser_typeA(code)
    parser.parse_program()