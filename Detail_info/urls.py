from django.urls import path
from .views import Detail, Favorite, Review, Random, Review_Delete

urlpatterns = [
    path('data/', Detail.as_view()),
    path('favorite/', Favorite.as_view()),
    path('review/', Review.as_view()),
    path('review/delete/', Review_Delete.as_view()),
    path('random/', Random.as_view())
]