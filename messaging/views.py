# messaging/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.db.models import Q # Para consultas OR
from .models import Conversation, Message
from .forms import MessageForm, NewConversationForm
from django.contrib.auth.models import User
from django.urls import reverse

# Vista para listar todas las conversaciones del usuario actual
@login_required
def conversation_list(request):
    # Obtiene todas las conversaciones en las que el usuario actual es un participante
    conversations = Conversation.objects.filter(participants=request.user).order_by('-updated_at')
    return render(request, 'messaging/conversation_list.html', {'conversations': conversations})

# Vista para ver una conversación específica y enviar mensajes
@login_required
def conversation_detail(request, conversation_id):
    # Obtiene la conversación o devuelve un 404 si no existe
    conversation = get_object_or_404(Conversation, id=conversation_id)

    # Asegura que el usuario actual sea un participante de la conversación
    if request.user not in conversation.participants.all():
        return redirect(reverse('messaging:conversation_list')) # Redirige si no es participante

    messages = conversation.messages.all() # Obtiene todos los mensajes de la conversación
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.conversation = conversation
            message.sender = request.user
            message.save()
            # Actualiza la marca de tiempo de la conversación para que aparezca arriba
            conversation.save() 
            return redirect(reverse('messaging:conversation_detail', args=[conversation.id]))
    else:
        form = MessageForm()
    
    return render(request, 'messaging/conversation_detail.html', {
        'conversation': conversation,
        'messages': messages,
        'form': form
    })

# Vista para iniciar una nueva conversación
@login_required
def new_conversation(request):
    if request.method == 'POST':
        form = NewConversationForm(request.POST, current_user=request.user)
        if form.is_valid():
            recipients = form.cleaned_data['recipients']
            initial_message_content = form.cleaned_data['initial_message']

            # Asegúrate de que el usuario actual también sea un participante
            all_participants = list(recipients) + [request.user]

            # Intenta encontrar una conversación existente con exactamente estos participantes
            existing_conversation = None
            for conv in Conversation.objects.filter(participants=request.user):
                conv_participants_ids = set(conv.participants.values_list('id', flat=True))
                if conv_participants_ids == set([user.id for user in all_participants]):
                    existing_conversation = conv
                    break

            if existing_conversation:
                conversation = existing_conversation
            else:
                # Crea una nueva conversación si no existe una con esos participantes
                conversation = Conversation.objects.create()
                conversation.participants.set(all_participants)
                conversation.save()

            # Crea el primer mensaje de la conversación
            Message.objects.create(
                conversation=conversation,
                sender=request.user,
                content=initial_message_content
            )
            
            return redirect(reverse('messaging:conversation_detail', args=[conversation.id]))
    else:
        form = NewConversationForm(current_user=request.user)
    
    return render(request, 'messaging/new_conversation.html', {'form': form})

