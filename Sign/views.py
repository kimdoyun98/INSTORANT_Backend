import jwt
from django.contrib.auth.hashers import check_password
from rest_framework.response import Response
from rest_framework.views import APIView

from .Serializer import Sign_Serializer
from .models import UserInfomation
from rest_framework.decorators import permission_classes, authentication_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


#@permission_classes([AllowAny])
class SignIn(APIView):
    def post(self, request):
        data = self.request.data
        username = data["username"]
        password = data["password"]

        user = UserInfomation.objects.filter(username=username).first()
        if user is None:
            return Response({"msg": "아이디가 없습니다."})
        if check_password(password, user.password):
            access_token = jwt.encode({"username": username, "name": user.name}, "secret", algorithm='HS256')
            return Response({"token": access_token, "msg": "success"})
        else:
            return Response({"msg": "비밀번호가 틀림"})


#@permission_classes([AllowAny])
class SignUp(APIView):
    def post(self, request):
        serializers = Sign_Serializer(data=request.data)
        if serializers.is_valid(raise_exception=True):
            if UserInfomation.objects.filter(username=serializers.data["username"]).exists():
                return Response({'msg': '이미 존재하는 아이디 입니다.'})

            serializers.create(request.data)

            return Response({'msg': '등록 완료'})


#@permission_classes([AllowAny])
class IDCheck(APIView):
    def post(self, request):
        print("IDCHeck")
        print(request.data["username"])
        name = request.data["username"]
        serializers = Sign_Serializer(data=request.data)

        if UserInfomation.objects.filter(username=name).exists():
            return Response({'msg': '이미 존재하는 아이디 입니다.'})
        else:
            return Response({'msg': '사용 가능한 아이디입니다.'})


#@permission_classes([AllowAny])
class Test(APIView):
    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        print(username, password)
        print(request.data)

        return Response({'status': 404})