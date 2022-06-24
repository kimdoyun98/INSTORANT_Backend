from django.contrib import admin
from django.urls import path, include
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Sign.urls')),
    path('search/', include('Search.urls')),
    path('detail/', include('Detail_info.urls')),
]
