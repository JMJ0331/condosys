from django import forms
from .models import ChatGroup, ChatMessage


class ChatGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['name']


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['sender', 'receiver', 'group', 'message']
