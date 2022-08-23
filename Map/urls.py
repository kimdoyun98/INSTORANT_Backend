from django.urls import path
from .views import Around_Restaurant

# /map/~
urlpatterns = [
    path('location/', Around_Restaurant.as_view()),
]