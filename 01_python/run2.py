# run2.py

def plus(n1, n2):
    print("안녕")

# 모듈에 있는 일부 함수, 클래스, 변수를 import -> 이름으로 호출 가능
from calc import plus as p, minus # 'calc의 plus, minus 두 함수를 사용한다' 선언
# from 사용할 것이 있는 경로 import 사용할 것(모듈, 모듈 내 함수, 클래스, 변수)

result1 = p(100, 200)
result2 = minus(200, 300)
print(result1, result2)

# 다른 패지키의 모듈 호출
import my_package.greet
my_package.greet.hello_eng()

from my_package import greet
greet.hello_kor()

from my_package import greet as g
g.hello_kor()

print(g.__version__)

# '패키지 -> 모듈 -> 함수'를 import
from my_package.greet import hello_kor, hello_eng 
hello_kor()
hello_eng()

# import를 하면 PYTHONPATH 경로에서 찾음. -> 현재 실행중인 디렉토리(01_python)
import sys
sys.path.append(r'c:\temp\lib') # PATHONPATH 에 new_package가 있는 경로 등록
from new_package import new_module
new_module.test_func()