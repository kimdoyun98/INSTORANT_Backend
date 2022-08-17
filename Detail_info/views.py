# 작성자-김도윤
# 상세페이지에서 작동하는 기능 API
# 2022.08.17 update

import jwt

from rest_framework.response import Response
from rest_framework.views import APIView
from Restaurant_recommend.utils import login_check

from Mongo import mycol
from Sign.models import UserFavorite, UserInfomation


# 상세정보 API
class Detail (APIView):
    def post(self, request):
        mongo_id = request.data.get('mongo_id')
        username = request.data.get("username")
        user_fav = UserFavorite.objects.filter(username=username, favor_id=mongo_id).exists()

        restaurant = mycol.find_one({'_id': mongo_id},
                                    {'_id': 0, 'Address': 1, "Name": 1, "Image": 1, "Score": 1, 'Menu': 1, 'Tag': 1})

        if user_fav is False:
            restaurant["fav"] = False
        else:
            restaurant["fav"] = True

        return Response(restaurant)


# 즐겨찾기 추기&삭제
class Favorite (APIView):
    @login_check  # Token 인증
    def put(self, request):  # 추가
        username = request.data.get("username")
        mongo_id = request.data.get("mongo_id")

        user = UserInfomation.objects.get(username=username)
        UserFavorite.objects.create(username=user, favor_id=mongo_id)

        return Response(status=200)

    @login_check
    def post(self, request):  # 삭제
        username = request.data.get("username")
        mongo_id = request.data.get("mongo_id")

        UserFavorite.objects.get(username=username, favor_id=mongo_id).delete()

        return Response(status=200)


# 즐겨찾기 목록 API
class Favorite_List(APIView):
    @login_check
    def post(self, request):
        print("Favorite_List")
        access_token = request.headers.get('Authorization', None)
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')

        fav_ids = UserFavorite.objects.filter(username=payload['username'])

        restaurant_list = []
        for fav_id in fav_ids:
            restaurant_list.append(mycol.find_one({"_id": fav_id.favor_id},
                                            {"_id": 1, "Name": 1, "Image": 1, "Score": 1}))

        return Response({'data': restaurant_list})