from django.contrib import auth
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.views import APIView
import pymongo
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


@permission_classes([AllowAny])#권한체크
class Search_Title (APIView):
    def Post(self, request):
        pass