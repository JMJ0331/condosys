"""
Django Channels consumers for real-time chat and notifications
"""
import json
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.utils import timezone
from .models import ChatMessage
from condosys.notifications.models import Notification
from condosys.accounts.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    """Consumer para chats privados entre usuarios"""
    
    async def connect(self):
        """Conexión WebSocket inicial"""
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'chat_{self.user_id}'
        
        # Verificar autenticación
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        # Unirse al grupo de chat del usuario
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Desconexión"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recibir mensaje del WebSocket"""
        try:
            data = json.loads(text_data)
            message = data.get('message')
            receiver_id = data.get('receiver_id')
            
            if not message or not receiver_id:
                return
            
            # Guardar mensaje en BD
            chat_message = await self.save_message(
                sender_id=str(self.scope["user"].id),
                receiver_id=receiver_id,
                message=message
            )
            
            # Enviar a receptor
            await self.channel_layer.group_send(
                f'chat_{receiver_id}',
                {
                    'type': 'chat.message',
                    'message': message,
                    'sender_id': str(self.scope["user"].id),
                    'sender_name': self.scope["user"].get_full_name(),
                    'timestamp': chat_message.created_at.isoformat(),
                }
            )
            
            # Confirmar envío a remitente
            await self.send(text_data=json.dumps({
                'type': 'message_sent',
                'message_id': str(chat_message.id),
                'status': 'delivered'
            }))
            
        except json.JSONDecodeError:
            pass

    async def chat_message(self, event):
        """Recibir mensaje del grupo y enviarlo al WebSocket"""
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def save_message(self, sender_id, receiver_id, message):
        """Guardar mensaje en base de datos"""
        try:
            receiver = User.objects.get(id=receiver_id)
            chat_msg = ChatMessage.objects.create(
                sender_id=sender_id,
                receiver=receiver,
                message=message
            )
            return chat_msg
        except User.DoesNotExist:
            return None


class GroupChatConsumer(AsyncWebsocketConsumer):
    """Consumer para chats de grupo"""
    
    async def connect(self):
        """Conexión a grupo"""
        self.group_name = self.scope['url_route']['kwargs']['group_name']
        self.room_group_name = f'group_{self.group_name}'
        
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()
        
        # Notificar que usuario se conectó
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'user.joined',
                'user_name': self.scope["user"].get_full_name(),
            }
        )

    async def disconnect(self, close_code):
        """Desconexión de grupo"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recibir y difundir mensaje de grupo"""
        try:
            data = json.loads(text_data)
            message = data.get('message')
            
            if not message:
                return
            
            # Guardar mensaje
            chat_message = await self.save_group_message(
                sender_id=str(self.scope["user"].id),
                group_name=self.group_name,
                message=message
            )
            
            # Enviar a todos en el grupo
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'group.message',
                    'message': message,
                    'sender_id': str(self.scope["user"].id),
                    'sender_name': self.scope["user"].get_full_name(),
                    'timestamp': chat_message.created_at.isoformat() if chat_message else None,
                }
            )
        except json.JSONDecodeError:
            pass

    async def group_message(self, event):
        """Recibir mensaje de grupo"""
        await self.send(text_data=json.dumps({
            'type': 'new_message',
            'message': event['message'],
            'sender_id': event['sender_id'],
            'sender_name': event['sender_name'],
            'timestamp': event['timestamp'],
        }))

    async def user_joined(self, event):
        """Notificar que usuario se unió"""
        await self.send(text_data=json.dumps({
            'type': 'user_joined',
            'user_name': event['user_name'],
        }))

    @database_sync_to_async
    def save_group_message(self, sender_id, group_name, message):
        """Guardar mensaje de grupo en BD"""
        chat_msg = ChatMessage.objects.create(
            sender_id=sender_id,
            group_name=group_name,
            message=message
        )
        return chat_msg


class NotificationConsumer(AsyncWebsocketConsumer):
    """Consumer para notificaciones en tiempo real"""
    
    async def connect(self):
        """Conexión para notificaciones"""
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_group_name = f'notifications_{self.user_id}'
        
        if not self.scope["user"].is_authenticated:
            await self.close()
            return
        
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        """Desconexión"""
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        """Recibir solicitudes (ej: marcar como leído)"""
        try:
            data = json.loads(text_data)
            action = data.get('action')
            
            if action == 'mark_as_read':
                notification_id = data.get('notification_id')
                await self.mark_notification_read(notification_id)
                
                await self.send(text_data=json.dumps({
                    'type': 'notification_marked',
                    'notification_id': notification_id,
                }))
        except json.JSONDecodeError:
            pass

    async def send_notification(self, event):
        """Enviar notificación al cliente"""
        await self.send(text_data=json.dumps({
            'type': 'notification',
            'notification_type': event['notification_type'],
            'title': event['title'],
            'message': event['message'],
            'related_id': event.get('related_id'),
            'timestamp': event['timestamp'],
        }))

    @database_sync_to_async
    def mark_notification_read(self, notification_id):
        """Marcar notificación como leída"""
        try:
            notification = Notification.objects.get(id=notification_id)
            notification.mark_as_read()
        except Notification.DoesNotExist:
            pass
