from django.urls import path
from .views import Search, Test

urlpatterns = [
    path('data/', Search.as_view()),
    path('test/', Test.as_view()),
]