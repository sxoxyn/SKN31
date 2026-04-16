# calc 모듈의 함수들을 호출 -> calc 모듈 import 필요
# import calc # 'calc 모듈을 사용하겠다' 선언.
import calc as c # 'calc 모듈을 c라는 이름으로 사용하겠다' 선언.

def test():
    pass
test() # 내 모듈에 있는 것은 그냥 사용.

# result = calc.plus(20, 30)
result = c.plus(20, 30) # 모듈 이름.사용할 함수() 호출
print(result)
# print(calc.minus(100, 20))
print(c.minus(100, 20))