# polls/urls.py
## polls app의 url conf 파일(- app별로 url 설정을 따로하기)

## urlconf: urlpatterns = [] 를 가지고 있어야 함
## Root UrlConf에 등록(설정)

from django.urls import path
from . import views

app_name = "polls"  # urls.py를 App별로 만들 때 식별하기 위한 이름

urlpatterns = [
    # 파라미터 1: url, 2: 함수, name="설정이름"(필수)

    # http://127.0.0.1:8000/polls/welcome -> welcome_polls() 호출
    path('welcome', views.welcome_polls, name="polls_welcome"), 

    # http://127.0.0.1:8000/polls/list -> vote_list() 호출
    path('list', views.vote_list, name="vote_list"), 

    # http://127.0.0.1:8000/polls/vote_form/paramete_id
    path("vote_form/<int:question_id>", views.vote_form, name="vote_form"), 
    # path parameter 설정: <type:변수명> -> type(int, str): 어떤 타입으로 읽을지, 변수명: 값을 받을 view의 파라미터 지정
    #   => <int:question_id>: 지정한 자리의 값을 int로 변환해 view 함수에 question_id 파라미터로 전달해라.
    
    path("vote", views.vote, name="vote"),

    path("vote_result/<int:question_id>", views.vote_result, name="vote_result"), # 투표 결과

    path("vote_create_old", views.vote_create_old, name="vote_create_old"), # 질문 등록

    path("vote_create", views.vote_create, name="vote_create"), # 질문 등록 - Form 사용
]