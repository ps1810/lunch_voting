from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import WinnerViewSet

router = DefaultRouter()
router.register(r'', WinnerViewSet, basename='winner')

urlpatterns = [
    path('', include(router.urls)),
]