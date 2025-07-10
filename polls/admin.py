from django.contrib import admin
from .models import *

# Register your models here.
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [ # 튜플들을 담는 배열 형태
        ("질문 섹션", {"fields": ["question_text"]}),
        ("생성일", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    
    list_display = ("question_text", "pub_date", "was_published_recently") # 튜플 형태(각 필드명을 입력)
    readonly_fields = ["pub_date"] # 배열 형태
    inlines = [ChoiceInline]
    list_filter = ["pub_date"]
    search_fields = ["question_text", "choice__choice_text"]

admin.site.register(Question, QuestionAdmin)