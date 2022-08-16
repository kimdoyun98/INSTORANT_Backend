from django.urls import path
from .views import SignUp, Test, SignIn, IDCheck
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token


# /account/~
urlpatterns = [
    path('signup/', SignUp.as_view()),
    path('idcheck/', IDCheck.as_view()),
    path('login/', SignIn.as_view()),
    path('test/', Test.as_view()),
]

# path('api/token/verify/', verify_jwt_token),  # JWT 토큰이 유효한 지 검증
# path('api/token/refresh/', refresh_jwt_token),  # JWT 토큰을 갱신할 때 사용