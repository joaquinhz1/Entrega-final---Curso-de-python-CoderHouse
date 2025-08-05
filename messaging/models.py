# messaging/models.py

from django.db import models
from django.contrib.auth.models import User

# Modelo para representar una conversación entre usuarios
class Conversation(models.Model):
    participants = models.ManyToManyField(User, related_name='conversations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at'] # Ordenar las conversaciones por la más reciente

    def __str__(self):
        # Muestra los nombres de usuario de los participantes en la conversación
        return f"Conversation between {', '.join([user.username for user in self.participants.all()])}"

# Modelo para representar un mensaje individual dentro de una conversación
class Message(models.Model):
    conversation = models.ForeignKey(Conversation, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['timestamp'] # Ordenar los mensajes por fecha y hora ascendente

    def __str__(self):
        return f"Message from {self.sender.username} in {self.conversation.id}"

