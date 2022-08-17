# 검색창에 검색 또는 키워드 선택시 음식점 목록 전송해주는 API

from rest_framework.response import Response
from rest_framework.views import APIView
from Mongo import mycol


class Search(APIView):
    def post(self, request):
        search_data = request.data.get('search_data')
        location = request.data.get('location')
        category = request.data.get('category')
        print(search_data)
        print("search_data : ", search_data, "location : ", location, "category : ", category)
        recommend_list = []

        if location:
            if category:
                if search_data:
                    # 검색어 : 위치 + (가게명 or Tag) / 위치 정보 / 카테고리
                    try:
                        city, title_tag = search_data.split(" ")
                        # 위치 + Tag 검색
                        if title_tag.find('#') != -1:
                            # Tag 추출 후 정제
                            data = list(title_tag.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#" + data[i]
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          "Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                            # Tag 가 여러 개일 때
                            if len(data) != 1:
                                return self.response_tag(data, recommend_list, restaurant_list)
                        # 위치 + 가게명 검색
                        else:
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          'Name': {'$regex': title_tag}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                        print("# 위치 + 가게명 or Tag + 위치 정보, 카테고리")
                        return self.response(recommend_list, restaurant_list)

                    # 검색어 : 위치 or 가게명 or 태그 / 위치 정보 / 카테고리
                    except ValueError:
                        location_split = list(location.split(" "))
                        if mycol.find_one({'City': search_data}):  # 위치
                            restaurant_list = mycol.find({"City": search_data, 'Category': category},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                        else:
                            # Tag 검색
                            if search_data.find('#') != -1:
                                # Tag 추출 후 정제
                                data = list(search_data.split("#"))
                                del data[0]
                                for i in range(len(data)):
                                    data[i] = "#" + data[i]
                                restaurant_list = mycol.find({'City': location_split[1], 'Category': category,
                                                              "Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                                if len(data) != 1:  # Tag 가 여러 개일 때
                                    return self.response_tag(data, recommend_list, restaurant_list)
                            # 가게명 검색
                            else:
                                restaurant_list = mycol.find({"City": location_split[1], 'Category': category,
                                                              "Name": {'$regex': search_data}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                        print("위치, 가게명, 태그 + 위치 정보, 카테고리")
                        return self.response(recommend_list, restaurant_list)

                # 검색창 비었을 때 -> 키워드 검색용
                else:
                    location_split = list(location.split(" "))
                    restaurant_list = mycol.find({"City": location_split[1], "Category": category},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    print("위치, 카테고리 O / 검색창 비었을 때")
                    return self.response(recommend_list, restaurant_list)

            # location O, category X
            else:
                # 검색어 : 위치 + (가게명 or Tag) / 위치 정보
                try:
                    city, title_tag = search_data.split(" ")
                    # 위치 + Tag 검색
                    if title_tag.find('#') != -1:
                        # Tag 추출 후 정제
                        data = list(title_tag.split("#"))
                        del data[0]
                        for i in range(len(data)):
                            data[i] = "#" + data[i]
                        restaurant_list = mycol.find({'City': city, "Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                        # Tag 가 여러 개일 때
                        if len(data) != 1:
                            return self.response_tag(data, recommend_list, restaurant_list)
                    # 위치 + 가게명 검색
                    else:
                        restaurant_list = mycol.find({'City': city, 'Name': {'$regex': title_tag}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    print("위치 + 가게명 or Tag + 위치 정보")
                    return self.response(recommend_list, restaurant_list)

                # 검색어 : 위치 or 가게명 or 태그 / 위치 정보
                except ValueError:
                    location_split = list(location.split(" "))

                    # 검색어가 위치일 경우
                    if mycol.find_one({'City': search_data}):
                        restaurant_list = mycol.find({"City": search_data},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    else:
                        # Tag 검색
                        if search_data.find('#') != -1:
                            # Tag 추출 후 정제
                            data = list(search_data.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#" + data[i]
                            restaurant_list = mycol.find({'City': location_split[1],
                                                          "Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                            # Tag 가 여러 개일 때
                            if len(data) != 1:
                                return self.response_tag(data, recommend_list, restaurant_list)
                        # 가게명 검색
                        else:
                            restaurant_list = mycol.find({"City": location_split[1],
                                                          "Name": {'$regex': search_data}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    print("위치, 가게명, 태그 + 위치 정보")
                    return self.response(recommend_list, restaurant_list)

        # location X
        else:
            if category:
                if search_data:
                    # 검색어 : 위치 + (가게명 or Tag) / 카테고리
                    try:
                        city, title_tag = search_data.split(" ")
                        # 위치 + Tag 검색
                        if title_tag.find('#') != -1:
                            # Tag 추출 후 정제
                            data = list(title_tag.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#" + data[i]
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          "Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                            # Tag 가 여러 개일 때
                            if len(data) != 1:
                                return self.response_tag(data, recommend_list, restaurant_list)
                        # 위치 + 가게명 검색
                        else:
                            restaurant_list = mycol.find({'City': city, 'Category': category,
                                                          'Name': {'$regex': title_tag}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                        print("위치 + 가게명 or Tag + 카테고리")
                        return self.response(recommend_list, restaurant_list)

                    # 검색어 : 위치 or 가게명 or 태그 / 카테고리
                    except ValueError:
                        # 검색어가 위치일 때
                        if mycol.find_one({'City': search_data}):
                            restaurant_list = mycol.find({"City": search_data, 'Category': category},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                        else:
                            # Tag 검색
                            if search_data.find('#') != -1:
                                # Tag 추출 후 정제
                                data = list(search_data.split("#"))
                                del data[0]
                                for i in range(len(data)):
                                    data[i] = "#" + data[i]
                                restaurant_list = mycol.find({'Category': category,
                                                              "Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                                if len(data) != 1:  # Tag 가 여러 개일 때
                                    return self.response_tag(data, recommend_list, restaurant_list)
                            # 가게명 검색
                            else:
                                restaurant_list = mycol.find({'Category': category,
                                                              "Name": {'$regex': search_data}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                        print("위치, 가게명, 태그  + 카테고리")
                        return self.response(recommend_list, restaurant_list)
                # 검색창 비었을 때 -> 키워드 검색용
                else:
                    restaurant_list = mycol.find({'Category': category},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    print("위치X 카테고리 O / 검색창 비었을 때")
                    return self.response(recommend_list, restaurant_list)
            # category X
            else:
                # 검색어 : 위치 + (가게명 or Tag)
                try:
                    city, title_tag = search_data.split(" ")
                    # 위치 + Tag 검색
                    if title_tag.find('#') != -1:
                        # Tag 추출 후 정제
                        data = list(title_tag.split("#"))
                        del data[0]
                        for i in range(len(data)):
                            data[i] = "#" + data[i]
                        restaurant_list = mycol.find({'City': city, "Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                        # Tag 가 여러 개일 때
                        if len(data) != 1:
                            return self.response_tag(data, recommend_list, restaurant_list)
                    # 위치 + 가게명 검색
                    else:
                        restaurant_list = mycol.find({'City': city, 'Name': {'$regex': title_tag}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    print("위치 + 가게명 or Tag")
                    return self.response(recommend_list, restaurant_list)

                # 검색엉 : 위치 or 가게명 or 태그
                except ValueError:
                    # 검색어가 위치일 때
                    if mycol.find_one({'City': search_data}):
                        restaurant_list = mycol.find({"City": search_data},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    else:
                        # Tag 검색
                        if search_data.find('#') != -1:
                            # Tag 추출 후 정제
                            data = list(search_data.split("#"))
                            del data[0]
                            for i in range(len(data)):
                                data[i] = "#"+data[i]
                            restaurant_list = mycol.find({"Tag": {'$regex': data[0]}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1}).sort('Score', -1)
                            # Tag 가 여러 개일 때
                            if len(data) != 1:
                                return self.response_tag(data, recommend_list, restaurant_list)
                        # 가게명 검색
                        else:
                            restaurant_list = mycol.find({"Name": {'$regex': search_data}},
                                                         {"_id": 1, "Name": 1, "Image": 1, "Score": 1})
                    print("마지막 response")
                    return self.response(recommend_list, restaurant_list)

    # Tag 미포함 검색어
    def response(self, recommend_list, restaurant_list):
        for restaurant in restaurant_list.sort('Score', -1):
            recommend_list.append(restaurant)

        return Response({'data': recommend_list})

    # Tag 포함 검색어
    def response_tag(self, data, recommend_list, restaurant_list):
        # temp_storage = []
        # for i in restaurant_list:
        #     for j in range(1, len(data)):  # 첫번재 태그 이후 태그들
        #         if i['Tag'].find(data[j]) != -1:
        #             if i in temp_storage:  # 중복 제거
        #                 pass
        #             else:
        #                 temp_storage.append(i)
        #         else:
        #             if j != 1:  # 두번 째 태그가 없으면 추가된 Document가 없음으로 pass
        #                 del temp_storage[-1]  # 태그들 중 하나라도 없으면 제외
        #             break
        # restaurant_list = temp_storage
        for restaurant in restaurant_list:
            recommend_list.append(restaurant)
        return Response({'data': recommend_list})