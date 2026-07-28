# polls/forms.py
from django import forms

# Form 클래스 정의 - forms.Form 상속
## 입력 폼들을 모아 정의한 클래스
## 입력 폼들 - (Form) Field: 개별 입력(input) 폼
## 일반적으로 <form> 안의 입력 폼들을 Form 클래스로 정의

####################
# 설문 질문 등록 폼
####################
class QuestionForm(forms.Form):
    # Form Field 정
    ## 변수명(요청 파라미터 name) = FormField(): 입력 형식
    question_text = forms.CharField( # 문자열 입력 폼 - <input type=text> (default)
        label="", # 입력폼에 대한 label 설정
        max_length=200, # 최대 입력 글자 수 <input max_length=200>
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    # 요청 파라미터 검증 메소드 => 업무 규칙(사용자 정의 규칙) 검증
    ## 메소드 이름 규칙
    ##  - clean_field이름: ex. clean_question_text() - 특정 필드의 입력값 검증
    ##  - clean(): 모든 Field들의 입력값들 검증
    ## 호출: Form의 각 Field들의 기본 검증 후 다 통과 시 clean메소드들 호출
    ### 기본 검증 ex. EmailField - 이메일 형식인지 검증, IntegerField - 정수인지 검증
    def clean_question_text(self):
        # cleaned_data['요청 파라미터 이름']: 기본 검증을 통과한 모든 요청 파라미터 값들
        txt = self.cleaned_data['question_text'].strip()

        # 질문은 5글자 이상
        if len(txt) < 5:
            # 검증 실패 -> ValidationError 발생
            raise forms.ValidationError("질문은 5글자 이상 입력하세요.")

        return txt

# 보기 입력
class ChoiceForm(forms.Form):
    choice_text = forms.CharField(
        label="",
        max_length=200,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    def clean_choice_text(self):
        txt = self.cleaned_data['choice_text'].strip()
        if not len(txt):
            raise forms.ValidationError("보기는 1글자 이상 입력하세요.")

        return txt

# FormSet 정의
# Form + Set: Form들의 집합
# ㄴㄴ
ChoiceFormSet = forms.formset_factory(
    ChoiceForm, # Form 클래스
    extra=2, # Form 클래스의 field들을 extra 개수만큼 반복해서 가짐
)