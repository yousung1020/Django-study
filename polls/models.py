from django.db import models
from django.utils import timezone
import datetime
from django.contrib import admin
from django.contrib.auth.models import User
# Create your models here.
# 모델 생성
# 모델을 테이블에 써 주기 위한 마이그레이션이라는걸 만든다.

# 질문: 여름에 놀러간다면 어디에 갈래?
# 산, 강, 바다

class Question(models.Model):
    question_text = models.CharField(max_length=200, verbose_name="질문")
    pub_date = models.DateTimeField(auto_now=True, verbose_name="생성일")
    owner = models.ForeignKey("auth.User", related_name="questions", on_delete=models.CASCADE, null=True)

    @admin.display(boolean=True, description="최근생성(하루기준)")
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        if self.was_published_recently():
            new_badge = "new!!!"
        else:
            new_badge = ""

        return f"{new_badge} 제목: {self.question_text}, 날짜: {self.pub_date}"
    

class Choice(models.Model):
    question = models.ForeignKey(Question, related_name="choices", on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return f"[{self.question.question_text}] {self.choice_text}"
    
class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
    voter = models.ForeignKey(User, on_delete=models.CASCADE)

    # 하나의 질문에는 하나의 투표자만이 존재할 수 있어야 함
    # question + voter 필드의 조합을 unique 속성으로 지정하여, 각 조합의 중복을 허가하지 않음
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["question", "voter"], name="unique_vote_for_questions")
        ]