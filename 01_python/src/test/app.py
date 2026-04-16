# app.py


from src.common import utils
print("app 테스트")
utils.util_func()

# 실행
# project root directory(01_python) 아래에서 실행
# python src\test\app.py => ModuleNotFoundError: No module named 'src'
# -> app.py 실행 - root directory : 실행시킨 app.py가 있는 디렉토리(test에서 src를 찾음)

# 해결
# python -m src.test.app
# 실행하는 디렉토리가 root directory가 돼서 import의 시작이 됨
# -m : 모듈로 실행히시키는 것.