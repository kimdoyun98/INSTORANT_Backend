from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from Mongo import mycol

@permission_classes([AllowAny])
class Detail (APIView):
    def post(self, request):
        mongo_id = request.data.get('mongo_id')

        restaurant = mycol.find_one({'_id': mongo_id},
                                    {'_id': 0, 'Address': 1, "Name": 1, "Image": 1, "Score": 1, 'Menu': 1, 'Tag': 1})

        return Response(restaurant)
