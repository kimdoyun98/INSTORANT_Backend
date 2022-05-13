from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from Mongo import mycol
# ToDO Tag가 여러 개일 때 / 카테고리 2개 이상일 때 /  가게이름 지점명 제외하고 검색할 때
#      ex) #a#b          ex) 술집, 밥집          ex) 역전할머니맥주


@permission_classes([AllowAny])
class Search(APIView):  # 검색 창에 위치와 가게명
    def post(self, request):
        search_data = request.data.get('search_data')
        location = request.data.get('location')
        category = request.data.get('category')

        if location:
            if category:
                if search_data:
                    try:  # 위치 + 가게명 or Tag
                        city, title_tag = search_data.split(" ")
                        if title_tag.find('#') != -1:  # Tag
                            tag = title_tag
                            restaurant_list = mycol.find({'City': city, 'Category': category, 'Tag': {'$regex': tag}})\
                                .sort('Score', -1)
                        else:  # 가게명
                            title = title_tag
                            restaurant_list = mycol.find({'City': city, 'Category': category, 'Name': title})\
                                .sort('Score', -1)

                        return self.response_1(restaurant_list)

                    except ValueError:  # 위치, 가게명, 태그
                        recommend_list = []
                        location_split = list(location.split(" "))
                        if mycol.find_one({'City': search_data}):  # 위치
                            restaurant_list = mycol.find({"City": search_data, 'Category': category}).sort('Score', -1)
                            return self.response_2(recommend_list, restaurant_list)
                        else:
                            if search_data.find('#') != -1:  # Tag
                                restaurant_list = mycol.find({"City": location_split[1], 'Category': category,
                                                              "Tag": {'$regex': search_data}}).sort('Score', -1)
                                return self.response_2(recommend_list, restaurant_list)
                            else:  # 가게명
                                restaurant_list = mycol.find({"City": location_split[1], 'Category': category,
                                                              "Name": search_data}).sort('Score', -1)
                                return self.response_2(recommend_list, restaurant_list)

                else:  # 검색창 비었을 때
                    location_split = list(location.split(" "))
                    restaurant_list = mycol.find({"City": location_split[1], "Category": category}).sort("Score", -1)
                    return self.response_1(restaurant_list)

            else:  # location O, category X
                try:  # 위치 + 가게명 or Tag
                    city, title_tag = search_data.split(" ")
                    if title_tag.find('#') != -1:  # Tag
                        tag = title_tag
                        restaurant_list = mycol.find({'City': city, 'Tag': {'$regex': tag}}) \
                            .sort('Score', -1)
                    else:  # 가게명
                        title = title_tag
                        restaurant_list = mycol.find({'City': city, 'Name': title}) \
                            .sort('Score', -1)

                    return self.response_1(restaurant_list)

                except ValueError:  # 위치, 가게명, 태그
                    recommend_list = []
                    location_split = list(location.split(" "))
                    if mycol.find_one({'City': search_data}):  # 위치
                        restaurant_list = mycol.find({"City": search_data}).sort('Score', -1)
                        return self.response_2(recommend_list, restaurant_list)
                    else:
                        if search_data.find('#') != -1:  # Tag
                            restaurant_list = mycol.find({"City": location_split[1],
                                                          "Tag": {'$regex': search_data}}).sort('Score', -1)
                            return self.response_2(recommend_list, restaurant_list)
                        else:  # 가게명
                            restaurant_list = mycol.find({"City": location_split[1],
                                                          "Name": search_data}).sort('Score', -1)
                            return self.response_2(recommend_list, restaurant_list)

        else:  # location X
            if category:
                if search_data:
                    try:  # 위치 + 가게명 or Tag
                        city, title_tag = search_data.split(" ")
                        if title_tag.find('#') != -1:
                            tag = title_tag
                            restaurant_list = mycol.find({'City': city, 'Category': category, 'Tag': {'$regex': tag}})\
                                .sort('Score', -1)
                        else:
                            title = title_tag
                            restaurant_list = mycol.find({'City': city, 'Category': category, 'Name': title})\
                                .sort('Score', -1)

                        return self.response_1(restaurant_list)

                    except ValueError:  # 위치, 가게명, 태그
                        recommend_list = []
                        if mycol.find_one({'City': search_data}):
                            restaurant_list = mycol.find({"City": search_data, 'Category': category}).sort('Score', -1)
                            return self.response_2(recommend_list, restaurant_list)
                        else:
                            if search_data.find('#') != -1:
                                restaurant_list = mycol.find({'Category': category, "Tag": {'$regex': search_data}})\
                                    .sort('Score', -1)
                                return self.response_2(recommend_list, restaurant_list)
                            else:
                                restaurant_list = mycol.find({'Category': category, "Name": search_data})\
                                    .sort('Score', -1)
                                return self.response_2(recommend_list, restaurant_list)
                # 검색창 비었을 때
                else:
                    restaurant_list = mycol.find({'Category': category}).sort('Score', -1)
                    return self.response_1(restaurant_list)
            # category X
            else:
                try:  # 위치 + 가게명 or Tag
                    city, title_tag = search_data.split(" ")
                    if title_tag.find('#') != -1:
                        tag = title_tag
                        restaurant_list = mycol.find({'City': city, 'Tag': {'$regex': tag}}).sort('Score', -1)
                    else:
                        title = title_tag
                        restaurant_list = mycol.find({'City': city, 'Name': title}).sort('Score', -1)

                    return self.response_1(restaurant_list)

                except ValueError:  # 위치, 가게명, 태그
                    recommend_list = []
                    if mycol.find_one({'City': search_data}):
                        restaurant_list = mycol.find({"City": search_data}).sort('Score', -1)
                        return self.response_2(recommend_list, restaurant_list)
                    else:
                        if search_data.find('#') != -1:
                            restaurant_list = mycol.find({"Tag": {'$regex': search_data}}).sort('Score', -1)
                            return self.response_2(recommend_list, restaurant_list)
                        else:
                            restaurant_list = mycol.find({"Name": search_data}).sort('Score', -1)
                            return self.response_2(recommend_list, restaurant_list)

    def response_1(self, restaurant_list):
        recommend_list = []
        for restaurant in restaurant_list:
            del restaurant['_id']
            recommend_list.append(restaurant)
        return Response({'data': recommend_list})

    def response_2(self, recommend_list, restaurant_list):
        for restaurant in restaurant_list:
            del restaurant['_id']
            recommend_list.append(restaurant)
        return Response({'data': recommend_list})
