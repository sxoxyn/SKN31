from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse # 응답 헤더
from django.db import transaction

from datetime import datetime
# 모델 클래스 import
from .models import Question, Choice

# View 함수 정의 - URL Conf에 등록(url mapping)
## URL Conf: 요청 URL과 View 함수 mapping하는 파일
## config/settings.py - ROOT_URLCONF에 설정된 파일(config.urls)

# 설문 welcome 페이지 응답하는 View 함수
def welcome_polls_backup(request): # 기본적으로 하나의 매개변수는 받아야 함
    now = datetime.now() # 실행시점 일시
    now_str = now.strftime("%Y-%m-%d %H:%M:%S") 
    # 응답 페이지 생성
    res_html = f"""<!doctype html>
<html>
    <head>
        <title>Polls - Welcome</title>
    </head>
    <body>
        <h1>Welcome</h1>
        <p>저희 설문 페이지에 방문해 주셔서 감사합니다.</p>
        현재 시간: {now_str}
    </body>
</html>
"""
    print("polls/welcome 실행")
    return HttpResponse(res_html)

def welcome_polls(request): # 기본적으로 하나의 매개변수는 받아야 함
    now = datetime.now() # 실행시점 일시
    now_str = now.strftime("%Y-%m-%d %H:%M:%S") 
    # 응답 : polls/welcome.html 템플릿 호출 -> html string
    ## template 호출하는 함수 - render()
    res_html = render(
        request,  # request
        "polls/welcome.html",  # template 파일 경로(app/templates 빼고 나머지 경로)
        {"now": now_str}  # context-value를 dictionary로 설정 - View가 Template에게 전달하는 값(객체)
    )
    print(res_html)  # HttpResponse
    return res_html

#########################################
# 설문 목록 조회
## 전체 question들을 조회해 목록으로 출력
## 요청 url: polls/list
## View 함수: vote_list
## template: polls/vote_list.html
#########################################
# View 함수 파라미터: 1 - request: HttpRequest 객체(HTTP 요청 정보)를 받는 변수(필수)
#                    2~ - path 파라미터를 받기 위한 변수들(옵션)
def vote_list(request):
    # DB에서 Question들을 조회
    question_list = Question.objects.all().order_by("-pub_date")

    # QuerySet [M, M, M]
    # 응답 화면 - Context Value로 question_list 전달
    return render(
        request, "polls/vote_list.html", {"question_list": question_list}
    )

###########################################################
# 설문 form 페이지 응답하는 View
## 요청 URL: /polls/vote_form/question_id
## view 함수: vote_form
## template: polls/vote_form.html
#
# question_id로 질문과 그 질문의 보기 조회
## question_id를 Path Parameter로 받음
## Path Parameter: url 경로 이용해 클라이언트 서버에 값 전달
# View의 두 번째 파라미터부터 path parameter 받을 변수들
## url conf에서 path parameter와 변수 연결
###########################################################
def vote_form(request, question_id):
    # question_id의 질문, 그 질문의 choice들을 조회
    try:
        question = Question.objects.get(pk=question_id)
        choice_list = question.choice_set.all()
        return render(
            request,
            "polls/vote_form.html",
            {"question": question, "choice_list": choice_list}
        )
    except:
        return render(
            request, 
            "polls/error.html", 
            {"error_message": f"{question_id}번 질문은 없는 질문입니다."}
        )

#######################################################################
# 설문 처리
## vote_form에서 선택한 보기의 vote값 1 증가
## 투표 결과 보여주는 화면을 응답
#
## 요청 URL: /polls/vote
## view 함수: vote
## 응답 : 정상 - (polls/vote_result.html) -> vote_result View로 Redirect 방식으로 이동
#         오류 - polls/vote_form.html(보기를 선택하지 않고 투표한 경우)
#######################################################################
# 요청 파라미터 조회
## GET: request.GET - Dictionary로 요청 파라미터 반환
## POST: request.POST - Dictionary로 요청 파라미터 반환

def vote(request):
    # choice 조회
    choice_id = request.POST.get("choice") # 없으면 None(인덱스(["choice"]) 시 없으면 exception)
    question_id = request.POST.get("question_id")

    if choice_id != None: # 선택된 보기가 넘어온 경우
        # choice.vote += 1
        choice = Choice.objects.get(pk=choice_id)
        choice.votes += 1
        choice.save() # update 쿼리 실행

        # Redirect 방식으로 vote_result View로 이동
        ## Web Browser에게 결과 보여주는 View로 이동하도록 요청 -> 새로고침해도 재투표 되는 것 막도록 함
        # url = "/polls/vote_result/"+str(question_id) # redirect할 URL

        # urls.py의 설정된 URL 조회 -> reverse(url mapping 설정 이름)
        # url mapping 설정 이름- app_name:name
        url = reverse("polls:vote_result", args=[question_id]) # path parameter: args에 순서대로 입력(path 뒤 "vote_result/**<int:question_id>**")
        print(">>>>>> reverse url:", url)
        return redirect(url) # 응답 상태코드가 302인 HttpResponse 반환

        # vote_result.html로 이동
        ## Question과 choice들 조회
        # question = Question.objects.get(pk=question_id)
        # choice_list = question.choice_set.all()
        # return render(
        #     request, "polls/vote_result.html", {"question": question, "choice_list": choice_list}
        # )

    else: # 보기를 선택하지 않고 투표한 경우
        # vote_form.html로 이동 - context value: Question과 그 choice들 + Error Message
        question = Question.objects.get(pk=question_id)
        choice_list = question.choice_set.all()
        return render(
            request, 
            "polls/vote_form.html", 
            {"question":question, "choice_list": choice_list, "error_message": "보기를 선택 후 투표하세요."}
        ) 

################################################
# 투표 결과 보여주는 View
#
# 요청 URL: polls/vote_result/<int:question_id>
# View 함수: vote_result
# 응답 Template: polls/vote_result.html
################################################
def vote_result(request, question_id):
    question = Question.objects.get(pk=question_id)
    choice_list = question.choice_set.all()
    return render(
        request, "polls/vote_result.html", {"question": question, "choice_list": choice_list}
    )


#################################################################
# 설문 질문 등록
#
# 요청 URL: /polls/vote_create
# View 함수: vote_create
## 요청 방식: GET - 등록 폼 응답
##           POST - 등록 처리
# 응답: GET - polls/vote_create.html (template)
#      POST - redirect => vote_list View 요청(질문 목록으로 이동)
#################################################################
# HTTP 요청 방식 조회: request.method (GET, POST, ...)

def vote_create_old(request):
    http_method = request.method
    print(">>>>>> Vote Create: ", http_method)

    if http_method == "GET":
        # 등록 폼 template 응답
        return render(request, "polls/vote_create.html")
    elif http_method == "POST":
        # 등록 처리
        ## 1. 요청 파라미터 조회, 검증
        ## 2. 처리 -> DB insert
        ## 3. 응답
        
        # 요청 파라미터 조회: resquest.GET, request.POST - dictionary 구현체
        ## 조회 메소드: get(이름) - 조회 결과가 한 개인 경우(return: str)
        ##              getlist(이름) - 하나의 이름으로 여러 개 값이 넘어오는 경우 
        question_text = request.POST.get('question_text') # str
        choice_list = request.POST.getlist('choice_text') # list[str]

        # 요청 파라미터 검증
        ## question_text로 넘어온 값이 없거나 (있는데 빈문자열이라면)
        if not question_text or (question_text and not question_text.strip()):
            return render(
                request, 
                "polls/vote_create.html", 
                {
                    "error_message": "질문은 한 글자 이상 입력하세요.",
                    "question_text": question_text,
                    "choice_list": choice_list
                }
                
            )

        ## 보기 요청 파라미터 검증 - 보기가 두 개 미만이라면
        if not choice_list or (choice_list and len([c for c in choice_list if c.strip()]) < 2):
            return render(
                request, 
                "polls/vote_create.html", 
                {
                    "error_message": "보기는 두 개 이상 입력하세요.",
                    "question_text": question_text,
                    "choice_list": choice_list
                }
            )

        # 질문/보기 등록 처리
        try: 
            ## transaction 처리 -> 질문&보기 모두 insert 되거나, 실패하면 모두 insert 안 되도록 보장
            with transaction.atomic(): # Transaction 시작 정의
                # with block을 정상적으로 실행 후 나오면 commit 실행
                #              실행 중 오류 발생 시 rollback 실행(DB의 상태를 시작하기 전(마지막 commit) 상태로 돌림)
                q = Question(question_text=question_text)
                q.save()

                for choice_text in choice_list:
                    choice = Choice(choice_text=choice_text, question=q) # id/vote는 자동입력
                    choice.save()
        except Exception as e:
            return render(request, "polls/error.html", {"error_message": "설문을 저장하는 도중 에러가 발생했습니다. 관리자에게 문의하세요."})


    # 응답: redirect 방식 -> 설문 목록으로 이동
    return redirect(reverse("polls:vote_list"))