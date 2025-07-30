from rest_framework import serializers
from polls.models import Question, Choice
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["choice_text", "votes"]

class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # 중첩된 시리얼라이저
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date", "owner", "choices"]

class UserSerializer(serializers.ModelSerializer):
    questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="question-detail")

    class Meta:
        model = User
        fields = ["id", "username", "questions"] 

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "두 패스워드가 일치하지 않습니다."})
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()

        return user

    class Meta:
        model = User
        fields = ["username", "password", "password2"]

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
    