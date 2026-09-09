from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, app_index

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    path('', app_index, name='notifications_index'),
    path('', include(router.urls)),
]
