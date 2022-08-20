from rest_framework import serializers

from Sign.models import UserReview


class Review_Serializer(serializers.ModelSerializer):
    class Meta:
        model = UserReview
        fields = ["review_id", "username", "restaurant_id", "content",
                  "image1", "image2", "image3", "score", "date_time"]