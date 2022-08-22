from rest_framework.response import Response
from rest_framework.views import APIView

from Day_recommend.Serializer import DayRecommends_Serializer
from Sign.models import DayRecommends


class Day_recommends(APIView):
    def post(self, request):  # 넘어오는 데이터 : city, category
        city = request.data.get("city")
        category = request.data.get("category")

        print(city, category)

        recommends = DayRecommends.objects.filter(city=city, category=category)

        serializers = DayRecommends_Serializer(recommends, many=True)

        return Response({"data": serializers.data})
