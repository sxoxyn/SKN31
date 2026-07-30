# account/form.py   
from django import forms

# ModelForm: forms.ModelForm 상속해 구현
#   - Meta class(Inner class로 정의)에서 어떤 Model을 이용해서 만들지, 그 Model의 어떤 Field를 입력폼으로 사용할지 설정
#   - Model에 없는 것을 입력 Field로 등록할 경우 class변수로 설정하면 됨(Form과 동일)

# Django에서 사용자 관리(등록, 수정)을 위해 제공하는 ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser

# 등록 화면에서 사용할 Form
class CustomUserCreationForm(UserCreationForm):

    # UserCreateFrom의 Field를 재정의하는 경우
    username = forms.CharField(label="ID", required=True, max_length=30)

    # UserCreateFrom에 없는 Field를 등록
    # age = forms.IntegerField(label="나이") # Meta.fields에 추가해야 사용 가능

    class Meta:

        model = CustomUser # 연결할 Model 지정
        
        # 입력 양식에 추가할 Model의 Field 정의
        ## [Field 선택, ...]: form 만드는 데 사용할 필드 선택
        ## "__all__": 모든 필드를 이용해 form 구성
        ### exclude = ['필드명']: 지정한 field 빼고 나머지
        fields = ["username", "password1", "password2", "name", "email", "birthday"] # , "age"]

        # 특정 Field들의 widget 변경
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"}) # DateInput: 날짜 형식 입력. type=date 정의
        }

    # 검증 메소드 추가(필요 시)
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError("이름은 두글자 이상 입력하세요.")
        return name

### 사용자 정보 변경 폼
class CustomUserChangeForm(UserChangeForm):
    # 비밀번호 변경 설정이 안 나오도록 처리
    password = None

    class Meta: 
        model = CustomUser
        fields = ["name", "email", "birthday"]
        widgets = {
            "birthday": forms.DateInput(attrs={"type": "date"})
        }

    # 검증 메소드 추가(필요 시)
    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 2:
            raise forms.ValidationError("이름은 두 글자 이상 입력하세요.")
        return name