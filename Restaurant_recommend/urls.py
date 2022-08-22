from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('Sign.urls')),
    path('search/', include('Search.urls')),
    path('detail/', include('Detail_info.urls')),
    path('map/', include('Map.urls')),
    path('day/', include('Day_recommend.urls')),
]
