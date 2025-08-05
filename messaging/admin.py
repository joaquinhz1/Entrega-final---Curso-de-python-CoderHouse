# messaging/admin.py

from django.contrib import admin
from .models import Conversation, Message

# Registra el modelo Conversation en el panel de administración
@admin.register(Conversation)
class ConversationAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    filter_horizontal = ('participants',) # Permite una interfaz mejor para seleccionar participantes

# Registra el modelo Message en el panel de administración
@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('conversation', 'sender', 'content', 'timestamp')
    list_filter = ('timestamp', 'sender')
    search_fields = ('content',)

