__version__ = 0.1 # 모듈의 변수

def plus(num1, num2):
    return num1 + num2

def minus(num1, num2):
    return num1 - num2

def multipy(num1, num2):
    return num1 * num2

def divid(num1, num2):
    return num1 / num2

# 실행 코드 -> calc가 main 모듈로 실행될 때만 실행되도록 처리.(모듈이 다른 곳에서 쓰일 것 같다면 아래 내용 꼭 필요)
print(__name__)
if __name__ == "__main__":
    result = minus(10, 5) # 함수 호출 -> 기본 : 같은 모듈에 정의 된 함수 호출
    print(result)

# python calc.py