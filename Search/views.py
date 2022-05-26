from django.contrib import auth
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from Mongo import mycol


@permission_classes([AllowAny])
class Search(APIView):
    def post(self, request):
        search_data = request.data.get('search_data')
        location = request.data.get('location')
        category = request.data.get('category')
        recommend_list = []

        if location:
            if category:
                if search_data:
                    try:  # 위치 + 가게명 or Tag + 위치 정보, 카테고리
                        city, title_tag = search_data.split(" ")
                        if title_tag.find('#') != -1:  # Tag
                            # Tag 추출 후 정제
                            data = list(title_tag.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#" + data[i]
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          "Tag": {'$regex': data[0]}}).sort('Score', -1)
                            if len(data) != 1:  # Tag 가 여러 개일 때
                                return self.response_tag(data, recommend_list, restaurant_list)
                        else:  # 가게명
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          'Name': {'$regex': title_tag}})

                        return self.response(recommend_list, restaurant_list)

                    except ValueError:  # 위치, 가게명, 태그 + 위치 정보, 카테고리
                        location_split = list(location.split(" "))
                        if mycol.find_one({'City': search_data}):  # 위치
                            restaurant_list = mycol.find({"City": search_data, 'Category': category})
                        else:
                            if search_data.find('#') != -1:  # Tag
                                # Tag 추출 후 정제
                                data = list(search_data.split("#"))
                                del data[0]
                                for i in range(len(data)):
                                    data[i] = "#" + data[i]
                                restaurant_list = mycol.find({'City': location_split[1], 'Category': category,
                                                              "Tag": {'$regex': data[0]}}).sort('Score', -1)
                                if len(data) != 1:  # Tag 가 여러 개일 때
                                    return self.response_tag(data, recommend_list, restaurant_list)
                            else:  # 가게명
                                restaurant_list = mycol.find({"City": location_split[1], 'Category': category,
                                                              "Name": {'$regex': search_data}})
                        return self.response(recommend_list, restaurant_list)

                else:  # 검색창 비었을 때
                    location_split = list(location.split(" "))
                    restaurant_list = mycol.find({"City": location_split[1], "Category": category})
                    return self.response(recommend_list, restaurant_list)

            else:  # location O, category X
                try:  # 위치 + 가게명 or Tag + 위치 정보
                    city, title_tag = search_data.split(" ")
                    if title_tag.find('#') != -1:  # Tag
                        # Tag 추출 후 정제
                        data = list(title_tag.split("#"))
                        del data[0]
                        for i in range(len(data)):
                            data[i] = "#" + data[i]
                        restaurant_list = mycol.find({'City': city, "Tag": {'$regex': data[0]}}).sort('Score', -1)
                        if len(data) != 1:  # Tag 가 여러 개일 때
                            return self.response_tag(data, recommend_list, restaurant_list)
                    else:  # 가게명
                        restaurant_list = mycol.find({'City': city, 'Name': {'$regex': title_tag}})

                    return self.response(recommend_list, restaurant_list)

                except ValueError:  # 위치, 가게명, 태그 + 위치 정보
                    location_split = list(location.split(" "))
                    if mycol.find_one({'City': search_data}):  # 위치
                        restaurant_list = mycol.find({"City": search_data})
                    else:
                        if search_data.find('#') != -1:  # Tag
                            # Tag 추출 후 정제
                            data = list(search_data.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#" + data[i]
                            restaurant_list = mycol.find({'City': location_split[1],
                                                          "Tag": {'$regex': data[0]}}).sort('Score', -1)
                            if len(data) != 1:  # Tag 가 여러 개일 때
                                return self.response_tag(data, recommend_list, restaurant_list)
                        else:  # 가게명
                            restaurant_list = mycol.find({"City": location_split[1],
                                                          "Name": {'$regex': search_data}})
                    return self.response(recommend_list, restaurant_list)

        else:  # location X
            if category:
                if search_data:
                    try:  # 위치 + 가게명 or Tag + 카테고리
                        city, title_tag = search_data.split(" ")
                        if title_tag.find('#') != -1:
                            # Tag 추출 후 정제
                            data = list(title_tag.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#" + data[i]
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          "Tag": {'$regex': data[0]}}).sort('Score', -1)
                            if len(data) != 1:  # Tag 가 여러 개일 때
                                return self.response_tag(data, recommend_list, restaurant_list)
                        else:
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          'Name': {'$regex': title_tag}})

                        return self.response(recommend_list, restaurant_list)

                    except ValueError:  # 위치, 가게명, 태그  + 카테고리
                        if mycol.find_one({'City': search_data}):
                            restaurant_list = mycol.find({"City": search_data, 'Category': category})
                        else:
                            if search_data.find('#') != -1:
                                # Tag 추출 후 정제
                                data = list(search_data.split("#"))
                                del data[0]
                                for i in range(len(data)):
                                    data[i] = "#" + data[i]
                                restaurant_list = mycol.find({'Category': category,
                                                              "Tag": {'$regex': data[0]}}).sort('Score', -1)
                                if len(data) != 1:  # Tag 가 여러 개일 때
                                    return self.response_tag(data, recommend_list, restaurant_list)
                            else:
                                restaurant_list = mycol.find({'Category': category,
                                                              "Name": {'$regex': search_data}})
                        return self.response(recommend_list, restaurant_list)
                # 검색창 비었을 때
                else:
                    restaurant_list = mycol.find({'Category': category})
                    return self.response(recommend_list, restaurant_list)
            # category X
            else:
                try:  # 위치 + 가게명 or Tag
                    city, title_tag = search_data.split(" ")
                    if title_tag.find('#') != -1:
                        # Tag 추출 후 정제
                        data = list(title_tag.split("#"))
                        del data[0]
                        for i in range(len(data)):
                            data[i] = "#" + data[i]
                        restaurant_list = mycol.find({'City': city, "Tag": {'$regex': data[0]}}).sort('Score', -1)
                        if len(data) != 1:  # Tag 가 여러 개일 때
                            return self.response_tag(data, recommend_list, restaurant_list)
                    else:
                        restaurant_list = mycol.find({'City': city, 'Name': {'$regex': title_tag}})

                    return self.response(recommend_list, restaurant_list)

                except ValueError:  # 위치, 가게명, 태그
                    if mycol.find_one({'City': search_data}):
                        restaurant_list = mycol.find({"City": search_data})
                    else:
                        if search_data.find('#') != -1:
                            # Tag 추출 후 정제
                            data = list(search_data.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#"+data[i]
                            restaurant_list = mycol.find({"Tag": {'$regex': data[0]}}).sort('Score', -1)
                            if len(data) != 1:  # Tag 가 여러 개일 때
                                return self.response_tag(data, recommend_list, restaurant_list)
                        else:
                            restaurant_list = mycol.find({"Name": {'$regex': search_data}})
                    return self.response(recommend_list, restaurant_list)

    def response(self, recommend_list, restaurant_list):
        for restaurant in restaurant_list.sort('Score', -1):
            del restaurant['_id']
            recommend_list.append(restaurant)
        return Response({'data': recommend_list})

    def response_tag(self, data, recommend_list,restaurant_list):
        temp_storage = []
        for i in restaurant_list:
            for j in range(1, len(data)):  # 첫번재 태그 이후 태그들
                if i['Tag'].find(data[j]) != -1:
                    if i in temp_storage:  # 중복 제거
                        pass
                    else:
                        temp_storage.append(i)
                else:
                    if j != 1:  # 두번 째 태그가 없으면 추가된 Document가 없음으로 pass
                        del temp_storage[-1]  # 태그들 중 하나라도 없으면 제외
                    break
        restaurant_list = temp_storage
        for restaurant in restaurant_list:
            del restaurant['_id']
            recommend_list.append(restaurant)
        return Response({'data': recommend_list})
