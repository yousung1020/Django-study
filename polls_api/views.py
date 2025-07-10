from polls.models import *
from polls_api.serializers import *
from rest_framework import generics

# Create your views here.
class QuestionList(generics.CreateAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)
    
    # def post(self, request, *args, **kwargs):
    #     return self.create(request, *args, **kwargs)

class QuestionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer

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