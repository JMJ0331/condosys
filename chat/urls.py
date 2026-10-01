from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ChatMessageViewSet, app_index, crear_grupo_chat, crear_mensaje_chat

router = DefaultRouter()
router.register(r'', ChatMessageViewSet, basename='chatmessage')

urlpatterns = [
    path('crear/grupo/', crear_grupo_chat, name='crear_grupo_chat'),
    path('crear/mensaje/', crear_mensaje_chat, name='crear_mensaje_chat'),
    path('', app_index, name='chat_index'),
    path('', include(router.urls)),
]
