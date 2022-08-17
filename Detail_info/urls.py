from django.urls import path
from .views import Detail, Favorite, Favorite_List

urlpatterns = [
    path('data/', Detail.as_view()),
    path('favorite/', Favorite.as_view()),
    path('favorite_list/', Favorite_List.as_view()),
]