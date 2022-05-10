from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Sign.urls')),
    path('', include('Search.urls')),
    path('api/token/', obtain_jwt_token),  # JWT 토큰을 발행할 때 사용
    path('api/token/verify/', verify_jwt_token),  # JWT 토큰이 유효한 지 검증
    path('api/token/refresh/', refresh_jwt_token),  # JWT 토큰을 갱신할 때 사용
]
