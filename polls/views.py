from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    context = {"questions": latest_question_list}

    return render(request, "polls/index.html", context)

def detail(request, question_id):
    # question = Question.objects.get(pk=question_id)
    question = get_object_or_404(Question, pk=question_id)

    return render(request, "polls/detail.html", {"question": question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        print(request.POST)
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, "polls/detail.html", {"question": question, "error_message": f"선택이 없습니다. id={request.POST["choice"]}"})
    else:
        selected_choice.votes = F("votes") + 1
        selected_choice.save()

    return HttpResponseRedirect(reverse("polls:result", args=(question_id,)))

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/result.html", {"question": question})

class SignupView(generic.CreateView):
    form_class = UserCreationForm
    # reverse, reverse_lazy 차이: reverse는 해당 함수가 호출되는 즉시 url 문자열 반환
    # reverse_lazy는  실제 값이 필요한 시점까지 url 생성을 미룸(lazy: 게으르게) 
    # reverse는 함수나 메서드 내부에서 사용한다.
    # reverse_lazy는 클래스 변수, 데코레이터, 함수의 기본 인자 등 코드가 파일 로드 시점(import 시점)에 평가될 때 사용한다.
    success_url = reverse_lazy("user-list") 
    template_name = "registration/signup.html"