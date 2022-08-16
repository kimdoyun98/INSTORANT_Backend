from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from Sign.models import UserInfomation


class Sign_Serializer(serializers.ModelSerializer):
    def create(self, vaildated_data):
        password = make_password(vaildated_data["password"])

        UserInfomation.objects.create(
            username=vaildated_data["username"],
            password=password,
            name=vaildated_data['name']
        )

    def validate(self, attrs):
        return attrs

    class Meta:
        model = UserInfomation
        fields = ("username", "password", "name")