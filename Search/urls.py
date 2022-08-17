from django.urls import path
from .views import Search

urlpatterns = [
    path('data/', Search.as_view()),
]