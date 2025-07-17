from rest_framework import serializers
from polls.models import Question
from django.contrib.auth.models import User

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date"]

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.PrimaryKeyRelatedField(many=True, queryset=Question.objects.all())

    class Meta:
        model = User
        fields = ["id", "username", "questions"] 
   
    # serializers.Serializer를 상속받았을 때는 아래와 같이 모든 것을 수동으로 정의해야 함
    
    # id = serializers.IntegerField(read_only=True)
    # question_text = serializers.CharField(max_length=200)
    # pub_date = serializers.DateTimeField(read_only=True)

    # # create: json으로부터 받아온 데이터를 저장할 때 사용
    # def create(self, validated_data):
    #     return Question.objects.create(**validated_data)
    
    # # instance: 기존에 있던 데이터
    # # validated_data: 수정 데이터
    # def update(self, instance, validated_data):
    #     instance.question_text = validated_data.get("question_text", instance.question_text) + "[시리얼라이저에서 업데이트]"
    #     instance.save()

    #     return instance
    