# 작성자-김도윤
# 상세페이지에서 작동하는 기능 API
# 2022.08.21 update
import random

import jwt
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView

from Detail_info.Serializer import Review_Serializer
from Restaurant_recommend.utils import login_check

from Common.Mongo import mycol
from Sign.models import UserFavorite, UserInfomation, UserReview


# 상세정보 API
class Detail (APIView):
    def post(self, request):
        restaurant_id = request.data.get('restaurant_id')
        access_token = request.headers.get('Authorization', None)

        if access_token == "":
            username = None
        else:
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            username = payload["username"]

        user_fav = UserFavorite.objects.filter(username=username, favor_id=restaurant_id).exists()

        restaurant = mycol.find_one({'_id': restaurant_id},
                                    {'_id': 1, 'Address': 1, "Name": 1, "Image": 1,
                                     "Score": 1, 'Tell_number': 1, 'Tag': 1})

        if user_fav is False:
            restaurant["fav"] = False
        else:
            restaurant["fav"] = True

        return Response(restaurant)


# 랜덤 음식점 데이터
class Random (APIView):
    def post(self, request):
        access_token = request.headers.get('Authorization', None)
        location = request.data.get("location")
        category = request.data.get("category")

        if location is None:
            return Response(status=500)

        restaurant = mycol.find({'City': location, 'Category': category},
                                {'_id': 1, 'Address': 1, "Name": 1, "Image": 1,
                                 "Score": 1, 'Tell_number': 1, 'Tag': 1})

        restaurant_list = list(restaurant)

        if len(restaurant_list) != 0:
            restaurant = random.sample(restaurant_list, 1)
            restaurant = restaurant[0]
            restaurant["fav"] = False

            if access_token is not None :
                mongo_id = restaurant["_id"]

                payload = jwt.decode(access_token, 'secret', algorithm='HS256')
                user_fav = UserFavorite.objects.filter(username=payload['username'], favor_id=mongo_id).exists()

                if user_fav is False:
                    restaurant["fav"] = False
                else:
                    restaurant["fav"] = True

        return Response(restaurant)


# 즐겨찾기 추기&삭제
class Favorite (APIView):
    @login_check
    def get(self, request):
        access_token = request.headers.get('Authorization', None)
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')
        fav_ids = UserFavorite.objects.filter(username=payload['username'])

        restaurant_list = []
        for fav_id in fav_ids:
            restaurant_list.append(mycol.find_one({"_id": fav_id.favor_id},
                                                  {"_id": 1, "Name": 1, "Image": 1, "Score": 1}))

        return Response({'data': restaurant_list})

    @login_check  # Token 인증
    def put(self, request):  # 추가
        restaurant_id = request.data.get("restaurant_id")

        access_token = request.headers.get('Authorization', None)

        if access_token == "":
            username = None
        else:
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            username = payload["username"]

        user = UserInfomation.objects.get(username=username)
        UserFavorite.objects.create(username=user, favor_id=restaurant_id)

        return Response(status=200)

    @login_check
    def post(self, request):  # 삭제
        restaurant_id = request.data.get("restaurant_id")

        access_token = request.headers.get('Authorization', None)

        if access_token == "":
            username = None
        else:
            payload = jwt.decode(access_token, 'secret', algorithm='HS256')
            username = payload["username"]

        UserFavorite.objects.get(username=username, favor_id=restaurant_id).delete()

        return Response(status=200)


# 리뷰(댓글) 조회, 삽입, 삭제
class Review(APIView):
    def post(self, request):  # 전체 조회
        restuarant_id = request.data.get("restaurant_id")

        review_data = UserReview.objects.filter(restaurant_id=restuarant_id)

        serializers = Review_Serializer(review_data, many=True)

        return Response({"data": serializers.data})

    @login_check
    def put(self, request):  # 삽입

        content = request.data.get("content")
        restaurant_id = request.data.get("restaurant_id")

        access_token = request.headers.get('Authorization', None)
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')

        user = UserInfomation.objects.get(username=payload['username'])

        time = datetime.now()
        time = time.strftime("%Y-%m-%d %H:%M:%S")

        UserReview.objects.create(username=user, restaurant_id=restaurant_id, content=content, date_time=time)

        review_data = UserReview.objects.filter(restaurant_id=restaurant_id)

        serializers = Review_Serializer(review_data, many=True)
        return Response({'data': serializers.data})

# 리뷰 삭제
class Review_Delete(APIView):
    @login_check
    def post(self, request):  # 삭제
        reviewid = request.data.get("review_id")

        access_token = request.headers.get('Authorization', None)
        payload = jwt.decode(access_token, 'secret', algorithm='HS256')

        UserReview.objects.get(review_id=reviewid, username=payload['username']).delete()

        review_data = UserReview.objects.all()
        serializers = Review_Serializer(review_data, many=True)

        return Response({'data': serializers.data})