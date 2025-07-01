from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.common.urls')),
    path('api/restaurants/', include('apps.restaurants.urls')),
    path('api/votes/', include('apps.voting.urls')),
    path('api/winners/', include('apps.winners.urls')),
]