from django.test import TestCase
from polls_api.serializers import QuestionSerializer, VoteSerializer
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.utils import timezone

# Create your tests here.

# view를 테스트 할 때는 django에서 제공하는 TestCase가 아닌, rest_framework가 제공하는 APITestCase를 사용해야 함.
class QuestionListTest(APITestCase):
    def setUp(self):
        self.question_data = {"question_text": "some question"}

        # 클래스 단이 아닌, 메서드 내부에서는 lazy가 아닌 그냥 reverse를 사용하면 된다.
        self.url = reverse("question-list")
    
    def test_create_question(self):
        user = User.objects.create(username="testuser", password="testpass")

        """
        # 이 부분 때문에 APITestCase를 사용함
        해당 기능은 사용자를 강제로 로그인 하게끔 함
        """
        self.client.force_authenticate(user=user)

        # 준비된 url로 question_data를 post 요청을 보냄. response에는 서버의 응답 객체가 저장됨
        response = self.client.post(self.url, self.question_data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 데이터베이스의 Question 테이블에 실제로 데이터가 1개 생성되었는지 확인
        self.assertEqual(Question.objects.count(), 1)
        
        question = Question.objects.first()

        # 데이터베이스에 저장된 질문의 question_text가 처음에 보냈던 데이터와 일치하는지 확인해서 데이터가 올바르게 저장되었는지 확인
        self.assertEqual(question.question_text, self.question_data["question_text"])

        # assertLess(a, b): a가 b보다 작은지 확인함. a < b 조건이 True이면 테스트 통과, 아니면 테스트 실패
        # 질문의 생성 시각과 현재 시각의 차이가 1초 미만인지 확인하여 pub_date가 올바르게 자동 생성되었는지 확인함
        """
        동작 원리
        1. timezone.now(): 테스트 코드가 해당 라인을 실행하는 그 현재 시각을 가져옴
        2. question.pub_date: Question 객체가 데이터베이스에 저장되는 순간의 시각
        3. timezone.now() - question.pub_date: 두 시간의 차이를 계산함. 결과는 timedelta 라는 시간 간격 객체가 됨. ex) 0.001초의 시간 간격
        4. .total_seconds(): timedelta 객체를 이해하기 쉬운 초 단위의 숫자로 변환
        5. 최종적으로 계산된 시간 차이가 1초보다 작은지 확인
        """
        self.assertLess((timezone.now() - question.pub_date).total_seconds(), 1)
    
    # 테스트 목적: 로그인하지 않은 사용자가 질문 생성을 시도할 때, 서버가 잘 거부하는지 검증
    def test_create_question_without_authentication(self):
        response = self.client.post(self.url, self.question_data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    # 테스트 목적: get 요청을 보냈을 때, QuestionList 뷰가 질문 목록을 올바른 데이터 구조로 잘 반환하는지 검증
    def test_list_questions(self):
        question = Question.objects.create(question_text="Question1")
        choice = Choice.objects.create(question=question, choice_text="choice1")
        Question.objects.create(question_text="Question2")

        response = self.client.get(self.url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # 미리 만들어둔 Question 객체의 갯수가 두 개인지 확인
        self.assertEqual(len(response.data), 2)
        # print(f"---------{response.data}\n")
        # 이거는.. 직접 데이터를 출력해서 구조를 파악하고 테스트 하는게 좋을 것
        self.assertEqual(response.data[0]["choices"][0]["choice_text"], choice.choice_text)

"""
TestCase 클래스
역할: 장고가 제공하는 테스트용 설계도 클래스이다.
각 테스트는 독립적인 트랜잭션 안에서 실행되어, 테스트가 끝난 후 데이터베이스를 원래 상태로 되돌림.
test_ 로 시작하는 이름의 메서드만 테스트로 인식하고 자동으로 실행해 줌.
"""

class VoteSerializerTestCase(TestCase):
    """
    setUp 메서드
    역할: 사전 준비를 위한 메서드이다. 각 test_ 메서드가 실행되기 직전에 매번 새로 호출되어, 테스트에 필요한 공통 데이터를 미리 생성하는 역할을 함.
    여러 테스트에서 반복되는 코드를 한곳에 모아서 중복을 없앨 수 있다.
    """
    def setUp(self):
        """
        self의 의미: 클래스로부터 생성된 자기 자신의 인스턴스를 가리킴.
        setUp 메서드에서 동일한 인스턴스를 공유하며 실행된다. 따라서 setUp에서 self로 저장해 둔 변수는
        이후에 실행되는 test_ 메서드에서 self. 으로 자유롭게 쓸 수 있다.
        """
        self.user = User.objects.create(username="testuser")
        self.question = Question.objects.create(question_text="abc", owner=self.user)
        self.choice = Choice.objects.create(question=self.question, choice_text="1")

    # 테스트 목적: VoteSerializer가 유효한 데이터를 받았을 때, 정상적으로 작동하는지 검증
    def test_vote_serializer(self):
        self.assertEqual(User.objects.all().count(), 1)
        data = {
            "question": self.question.id,
            "choice": self.choice.id, 
            "voter": self.user.id
        }

        serializer = VoteSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        # save()는 모델 인스턴스를 반환함
        # VoteSerializer를 통해 역직렬화 했으므로, Vote 모델 인스터스가 반환됨
        vote = serializer.save()

        """
        assert로 시작하는 메서드
        역할: 테스트를 단언한다(assertion). 즉 코드의 실행 결과가 내가 예상한 값과 일치하는지 검증하는 역할을 함.
        self.assertEqual(a, b): a와 b가 같으면 테스트 통과, 다르면 테스트 실패
        self.assertTrue(a): a가 True이면 통과, False면 테스트 실패
        self.assertFalse(a): a가 False면 통과, True면 테스트 실패

        해당 메서드들(단언문)을 모두 통과해야만 최종적으로 테스트가 성공함.
        """
        self.assertEqual(vote.question, self.question)
        self.assertEqual(vote.choice, self.choice)
        self.assertEqual(vote.voter, self. user)
    
    # 테스트 목적: VoteSerializer가 중복된 투표 데이터를 받았을 때, 이를 잘 거부하는지 검증
    def test_vote_serializer_with_duplicate_vote(self):
        # setUp 메서드가 각 테스트에 독립적으로 데이터를 공유함을 확인
        # self.assertEqual(User.objects.all().count(), 1)

        choice1 = Choice.objects.create(
            question=self.question,
            choice_text="2"
        )

        # 데이터베이스에 특정 사용자가 특정 질문에 한 투표를 미리 만들어 둠
        Vote.objects.create(question=self.question, choice=self.choice, voter=self.user)

        # 동일한 사용자가 동일한 질문에 다른 선택지로 투표하는 데이터를 준비
        data = {
            "question": self.question.id,
            "choice": choice1.id, 
            "voter": self.user.id
        }

        """
        VoteSerializer에 정의되어 있는 다음의 유효성 검증을 통해 is_valid() 했을 때, False를 반환하는지 확인

        UniqueTogetherValidator(
                # queryset: 검사 대상이 되는 데이터 범위
                queryset=Vote.objects.all(),
                # fields: 어떤 필드들의 조합이 유일해야 하는지를 지정
                fields = ["question", "voter"]
            )
        """

        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())
    
    def test_vote_serializer_with_unmatched_and_choice(self):
        question2 = Question.objects.create(
            question_text="abc",
            owner=self.user
        )
        choice2 = Choice.objects.create(
            question=question2,
            choice_text="1"
        )
        data = {
            "question": self.question.id,
            "choice": choice2.id,
            "voter": self.user.id,
        }

        serializer = VoteSerializer(data=data)
        self.assertFalse(serializer.is_valid())

class QuestionSerializerTestCase(TestCase):
    def test_with_valid_data(self):
        # self.assertEqual(1, 2)
        serializer = QuestionSerializer(data={"question_text": "abc"})
        self.assertEqual(serializer.is_valid(), True)
        new_question = serializer.save()
        self.assertIsNotNone(new_question.id)

    def test_with_invalid_data(self):
        serializer = QuestionSerializer(data={"question_text": ""})
        self.assertEqual(serializer.is_valid(), False)
 
    # def some_method(self):
    #     print("this is some method")
