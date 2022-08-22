from django.urls import path
from .views import Search

# /search/~
urlpatterns = [
    path('data/', Search.as_view()),
]