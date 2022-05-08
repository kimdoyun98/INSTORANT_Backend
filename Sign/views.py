from django.contrib import auth
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User_Infomation
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication

# class SignIn(APIView):
#     def post(self, request):
#
#
#         data = self.request.data
#         user_id = data["user_id"]
#         user_pw = data["user_pw"]
#         try:
#             user = auth.authenticate(username=user_id, password=user_pw)
#
#             if user is not None:
#                 auth.login(request, user)
#                 return Response({'msg': '로그인 성공', 'data': user_id})
#         except:
#             return Response(dict(msg="로그인 실패"))


# class SignOut(APIView):
#     def get(self, request):
#         logout(request)
#         return Response({'msg': '로그아웃'})

@permission_classes([AllowAny])
class SignUp(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = User_Infomation.objects.create_user(username=username, password=password)
        user.save()

        return Response({'msg': '등록 완료'})