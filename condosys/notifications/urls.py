from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import NotificationViewSet, app_index, crear_notificacion

router = DefaultRouter()
router.register(r'', NotificationViewSet, basename='notification')

urlpatterns = [
    path('crear/', crear_notificacion, name='crear_notificacion'),
    path('', app_index, name='notifications_index'),
    path('', include(router.urls)),
]