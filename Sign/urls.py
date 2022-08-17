from django.urls import path
from .views import SignUp, SignIn, IDCheck


# /account/~
urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('idcheck/', IDCheck.as_view()),
    path('login/', SignIn.as_view()),
]