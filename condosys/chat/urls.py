from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatMessageViewSet, app_index

router = DefaultRouter()
router.register(r'', ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('', app_index, name='chat_index'),
    path('', include(router.urls)),
]
