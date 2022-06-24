from django.urls import path
from .views import Detail

urlpatterns = [
    path('data/', Detail.as_view()),
]