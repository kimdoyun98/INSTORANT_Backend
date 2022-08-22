from rest_framework import serializers

from Sign.models import DayRecommends


class DayRecommends_Serializer(serializers.ModelSerializer):
    class Meta:
        model = DayRecommends
        fields = ["restaurant_id", "city", "category", "image", "address", "name"]