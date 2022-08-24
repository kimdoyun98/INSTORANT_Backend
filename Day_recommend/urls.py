from django.urls import path
from .views import Day_recommends

# /day/~
urlpatterns = [
    path('recommend/', Day_recommends.as_view()),
]