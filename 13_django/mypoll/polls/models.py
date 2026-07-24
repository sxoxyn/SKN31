from django.db import models

# 모델 클래스 정의 = Question설문 질문), Choice설문 보기)
## - Model 상속
## - class 이름 : 단수형
## - class 변수로 Field 정의(Field -(연결)- Table의 컬럼)
### - Field : 필드 이름(컬럼 이름, instance 변수 이름) = Field 객체(컬럼 설정)
## - primary key Field가 없으면 자동으로 생성
### - Field명 : id, type : 양의 정수형, 1씩 자동 증가
### - 특정 Field를 PK로 설정하려면 'XXXField(primary_key=True)'로 설정

# Question Model Class 정의
class Question(models.Model):                            # create table Question(
    # 질문 문장
    question_text = models.CharField(max_length=200)     #   question_text, -> varchar(200)
    # 질문 등록 일시
    pub_date = models.DateTimeField(auto_now_add=True)   #   pub_date -> datetime
    # auto_now_add: insert 시점의 일시를 자동으로 입력

    def __str__(self):
        return f"{self.pk}. {self.question_text}"
        # self.pk : Primary Key Field의 값을 조회

# Choice 모델 클래스
class Choice(models.Model):
    choice_text = models.CharField(max_length=200)
    votes = models.PositiveIntegerField(default=0)
    question = models.ForeignKey(
        Question,  # 참고 Model 클래스 - Question
        on_delete=models.CASCADE  # 부모 데이터가 삭제되면 같이 삭제
    )  
    def __str__(self):
        return f"{self.pk}. {self.choice_text}"

# 모델 클래스를 최초 생성, 수정한 경우 Database에 적용
#   1. python manage.py makemigrations [app이름] (- app 이름을 주면 그 app에만 적용)
#    - DB에 적용할 것들을 코드로 작성
#   2. python manage.py migrate - DB에 적용

# 테이블 이름 : app이름_class이름 (ex. polls_question)