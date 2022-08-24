from rest_framework.response import Response
from rest_framework.views import APIView


from Common.Mongo import mycol


# 내 현재 위치 주변 음식점
class Around_Restaurant(APIView):
    def post(self, request):
        x = request.data.get("x")
        y = request.data.get("y")

        around_restaurant_list = mycol.find({
             "location": {
                 "$near": {
                    "$geometry": {"type": "Point",  "coordinates": [x, y]},
                    "$maxDistance": 1000
                   }
               }
            }
        )

        json_restaurant_list = []
        for restaurant in around_restaurant_list:
            json_restaurant_list.append(restaurant)

        return Response({"data": json_restaurant_list})