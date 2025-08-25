from rest_framework import serializers
from polls.models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

# VoteList에서 나의 투표 내역을 보여주거나, 새로운 투표를 생성할 때 사용됨
class VoteSerializer(serializers.ModelSerializer):
    voter = serializers.ReadOnlyField(source="voter.username")

    class Meta:
        model = Vote
        fields = ["id", "question", "choice", "voter"]

# Question의 상세 정보를 보여줄 때, 각 선택지의 내용을 어떤 형식으로 보여줄지 정의함
class ChoiceSerializer(serializers.ModelSerializer):
    # 값이 메서드에 의해서 결정되는 필드
    # 즉, 데이터베이스 필드에서 직접 가져오는 것이 아니라, get_vote_count 메서드를 호출한 결과로 채워짐
    vote_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Choice
        fields = ["choice_text", "vote_count"]
    
    # obj: 실제 모델 객체
    def get_vote_count(self, obj):
        return obj.vote_set.count()

# 질문 목록이나 상세 정보를 보여주는 api의 핵심적인 데이터 형식을 정의함.
class QuestionSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    # 중첩된 시리얼라이저
    # Question 정보를 보여줄 때, 관련된 choices 정보도 함께 보여주라는 의미.
    choices = ChoiceSerializer(many=True, read_only=True)
    class Meta:
        model = Question
        fields = ["id", "question_text", "pub_date", "owner", "choices"]

# 사용자의 목록이나 상제 정보를 보여줄 때 사용됨.
class UserSerializer(serializers.ModelSerializer):
    # 해당 사용자가 작성한 questions 목록을 보여줄 때, 질문의 모든 데이터를 보여주는 것이 아닌 상세 정보 페이지로 가는 url을 보여줌
    questions = serializers.HyperlinkedRelatedField(many=True, read_only=True, view_name="question-detail")

    class Meta:
        model = User
        fields = ["id", "username", "questions"] 

# 회원가입 데이터 유효성 검사 및 생성
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    # 역직렬화 과정 중에, is_valid()가 호출되고 마지막 단계에 실행됨
    # validate가 파라미터로 받는 attrs의 내용: 필드 레벨 검사를 통과한 검증된 데이터들만 모인 딕셔너리
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
    