"""
Django Channels routing for WebSocket chat
"""
from django.urls import re_path
from . import consumers

websocket_urlpatterns = [
    # Private chat: ws://localhost:8000/ws/chat/{user_id}/
    re_path(r'ws/chat/(?P<user_id>[\w-]+)/$', consumers.ChatConsumer.as_asgi()),
    
    # Group chat: ws://localhost:8000/ws/group/{group_name}/
    re_path(r'ws/group/(?P<group_name>[\w-]+)/$', consumers.GroupChatConsumer.as_asgi()),
    
    # Notifications: ws://localhost:8000/ws/notifications/{user_id}/
    re_path(r'ws/notifications/(?P<user_id>[\w-]+)/$', consumers.NotificationConsumer.as_asgi()),
]
