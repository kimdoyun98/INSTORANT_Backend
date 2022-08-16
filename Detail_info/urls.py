from django.urls import path
from .views import Detail, Favorite

urlpatterns = [
    path('data/', Detail.as_view()),
    path('favorite/', Favorite.as_view()),
]