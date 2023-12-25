import sys
from Parser_statements import ParsingStatements, ParsingToken

############### <진입점> #################

# code = "x := (5 + 3) ;y := x * 2+((3));z := 3; k := 2+3/0-4*x;x := 2+3*((8))*3+y;"
# ParsingStatements(code)

def main():

    verbose = False
    filename = ""

    # 두 번째 인자 확인
    if sys.argv[1] == "-v":
        verbose = True
        filename = sys.argv[2]  # 세 번째 인자가 파일 이름
    else:
        filename = sys.argv[1]  # 두 번째 인자가 파일 이름
    
    # 파일 처리
    process_file(filename, verbose)

def process_file(filename, verbose):
    if verbose:
        with open(filename, 'r') as file:
            data = file.read()
            ParsingToken(data)
    else:
        print(f"Processing file: {filename}")
        with open(filename, 'r') as file:
            data = file.read()
            ParsingStatements(data)

# 현재 파일이 실행되면 코드 실행
if __name__ == "__main__":
    main()