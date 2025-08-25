from rest_framework import permissions

class IsOwnerOrReadOnly(permissions.BasePermission):
    # has_permission은 1차 관문으로써 뷰 레벨 권한을 확인함.
    # 언제 호출? 뷰의 핵심 로직이 실행되기 전, 특정 객체(obj)를 데이터베이스에서 가져오기 전에 호출됨.
    # 무엇을 검사? 이 사용자가 이 뷰 자체에 접근할 자격이 있는가와 같은 전역적인 규칙을 검사함.
    # 주요 검사 내용: 로그인한 사용자인가?(IsAutenticated), 읽기 요청인가?(IsAuthenticatedOrReadOnly)
    # 관리자(admin)인가? 등등
    # 비유: 회사 입구에서 신분증(로그인 여부)나 직원 명찰(관계자 여부)을 검사하는 것과 비슷함. 일단 들어갈 자격이 있는지 확인!

    # has_object_permission은 2차 관문으로써 객체 레벨 권한을 확인함.
    # 언제 호출? 뷰가 get_object()를 통해 데이터베이스에서 특정 객체(obj)를 성공적으로 가져온 직후에 호출됨.
    # 따라서 QuestionDetail처럼 특정 객체 하나를 다루는 뷰에서만 의미가 있음. QuestionList 같은 목록 뷰에서는 호출되지 않음.
    # 무엇을 검사? 이 사용자가 방금 가져온 객체(obj)를 다룰 권한이 있는가? 와 같은 개별적인 규칙을 검사함.
    # 주요 검사 내용: 이 객체의 소유자인가?(IsOwnerOrReadOnly), 이 객체에 대해 특정 권한 플래그를 가지고 있는가?
    # 비유: 회사 안의 개발팀 회의룸에 들어가려고 할 때, 이 회사의 개발자가 맞습니까? 라고 개별적으로 확인하는 곳과 비슷하다.
    # 회사에 들어왔다고 해서 모든 곳에 들어갈 수 없는 것과 같다.

    # 파라미터 상세 정보
    # request: drf에 의해 가공된 Request 객체이다.(request.user, request.data etc...)
    # view: 현재 이 권한 검사를 호출한 뷰 클래스의 인스턴스이다.(QuestionDetail 같은 뷰 클래스의 객체)
    # obj(가장 중요): 뷰가 데이터베이스에서 조회해 온 실제 모델 객체이다.(뷰 클래스에서 queryset이나 get_queryset 메서드 등으로 가져온 실제 모델 객체)
    def has_object_permission(self, request, view, obj):
        # read only는 항상 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        
        return obj.owner == request.user
    
class IsVoter(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # 무조건 투표를 등록한 사람만 접근할 수 있도록 권한 설정을 함(crud에 대한)
        return obj.owner == request.user