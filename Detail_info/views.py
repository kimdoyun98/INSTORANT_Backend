from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from Restaurant_recommend.utils import login_check

from Mongo import mycol
from Sign.models import UserFavorite, UserInfomation


#@permission_classes([AllowAny])
class Detail (APIView):
    def post(self, request):
        mongo_id = request.data.get('mongo_id')
        username = request.data.get("username")
        print(type(mongo_id))
        print("헤더 : ", request.META.get('HTTP_AUTHORIZATION'))
        user_fav = UserFavorite.objects.filter(username=username, favor_id=mongo_id).exists()
        print(user_fav)

        restaurant = mycol.find_one({'_id': mongo_id},
                                    {'_id': 0, 'Address': 1, "Name": 1, "Image": 1, "Score": 1, 'Menu': 1, 'Tag': 1})

        if user_fav is False:
            restaurant["fav"] = False
        else:
            restaurant["fav"] = True

        return Response(restaurant)


#@permission_classes([AllowAny])

class Favorite (APIView):
    @login_check
    def put(self, request):
        username = request.data.get("username")
        mongo_id = request.data.get("mongo_id")

        user = UserInfomation.objects.get(username=username)
        UserFavorite.objects.create(username=user, favor_id=mongo_id)

        return Response(status=200)

    @login_check
    def post(self, request):
        username = request.data.get("username")
        mongo_id = request.data.get("mongo_id")

        UserFavorite.objects.get(username=username, favor_id=mongo_id).delete()

        return Response(status=200)
