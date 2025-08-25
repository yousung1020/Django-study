from polls.models import *
from polls_api.serializers import *
from rest_framework import generics, permissions
from django.contrib.auth.models import User
from .permissions import IsOwnerOrReadOnly, IsVoter

# 내가 작성한 vote들만 보여주게끔 함

# queryset 클래스 변수: 정적범위
# 뷰 클래스가 처음 로드될 때 한 번만 결정됨. 모든 요청에 대해서 항상 동일한 데이터 집합을 대상으로 함. ex) Question.objects.all()

# get_queryset() 메서드: 동적범위
# 매 요청이 들어올 때마다 새로 호출됨. request 객체에 접근할 수 있으므로, 요청 정보에 따라 매번 다른 데이터 집합을 반환할 수 있다. 

# api 역할: 나의 투표 내역 조회
class VoteList(generics.ListCreateAPIView):
    serializer_class = VoteSerializer

    # 오직 로그인한 사용자만 해당 api에 접근할 수 있음
    permission_classes = [permissions.IsAuthenticated]

    # get 요청 처리
    # queryset = Vote.objects.all() 처럼 전체 투표 목록이 아닌, 현재 요청을 보낸 사용자가 생성한 투표만 필터링하여 개인화된 목록을 반환
    def get_queryset(self, *args, **kwargs):
        return Vote.objects.filter(voter=self.request.user)
    
    # post 요청 처리(새로운 투표 생성)
    # 데이터베이스에 저장할 때, 현재 로그인한 사용자의 투표들만 저장
    # 동작 순서
    # 1. 클라이언트가 보낸 request.data를 VoteSerializer(data=...)으로 시리얼라이저를 초기화함.
    # 2. serializer.is_valid()를 호출해서 데이터 유효성 검사를 진행함.
    # 3. 유효성 검사를 통과하면, perform_create(self, serializer) 메서드를 호출함.
    # 4. 해당 메서드 안에서 save가 진행됨

    # 왜 필요한가? 클라이언트는 투표할 때 request.data에 어떤 질문과 어떤 선택지에 투표할지만 담아서 보냄.
    # "누가" 투표하는지에 대한 정보(voter)는 보내지 않음. 이 정보는 신뢰할 수 없는 클라이언트 측이 아니라, 서버가 인증한 시스템을 통해 확인한
    # request.user를 사용해야 안전하기 때문.
    # 그래서 save 인수에 voter(모델의 필드)에 request.user 데이터를 직접적으로 넣어서 저장함. 기존에 역직렬화된 데이터들에서 voter 정보를 자동으로 병합!
    def perform_create(self, serializer):
        serializer.save(voter=self.request.user)

# api 역할: 사용자의 특정 투표 내역 상세/수정/삭제
class VoteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permissions_classes = [permissions.IsAuthenticated, IsVoter]

# api 역할: 전체 질문 목록 보여주기와 새 질문 생성
class QuestionList(generics.ListCreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

# api 역할: 특정 질문에 대해 상세/수정/삭제
class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

# api 역할: 사용자 정보 조회(읽기 전용)
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# 아직은 위와 동일함
class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# api 역할: 회원가입
class RegisterUser(generics.CreateAPIView):
    serializer_class = RegisterSerializer  

    # def get(self, request, *args, **kwargs):
    #     return self.retrieve(request, *args, **kwargs)

    # def put(self, request, *args, **kwargs):
    #     return self.update(request, *args, **kwargs)

    # def delete(self, request, *args, **kwargs):
    #     return self.destroy(request, *args, **kwargs)

# 해당 메서드가 get, post 요청을 처리할 것이라고 암시함
# @api_view(["GET", "POST"])
# def question_list(request):
#     if(request.method == "GET"):       
#         questions = Question.objects.all()
#         # Question 객체가 하나가 아니기 때문에(all) many 옵션을 true로 해주어야 한다.
#         serializer = QuestionSerializer(questions, many=True)

#         return Response(serializer.data)
    
#     if(request.method == "POST"):
#         serializer = QuestionSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

# @api_view(["GET", "PUT", "DELETE"])
# def question_detail(request, id):
#     question = get_object_or_404(Question, pk=id)
#     if request.method == "GET":
#         serializer = QuestionSerializer(question)
#         return Response(serializer.data)
    
#     if request.method == "PUT":
#         serializer = QuestionSerializer(question, data=request.data)

#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
#     if request.method == "DELETE":
#         question.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)