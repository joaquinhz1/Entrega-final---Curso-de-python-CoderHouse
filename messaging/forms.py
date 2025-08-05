# messaging/forms.py

from django import forms
from .models import Message
from django.contrib.auth.models import User

# Formulario para enviar un mensaje dentro de una conversación existente
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content'] # Solo necesitamos el contenido del mensaje
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe tu mensaje aquí...'}),
        }

# Formulario para iniciar una nueva conversación con uno o más usuarios
class NewConversationForm(forms.Form):
    # Permite seleccionar múltiples usuarios para la conversación
    # Excluye al usuario actual de las opciones
    recipients = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        widget=forms.CheckboxSelectMultiple, # O forms.SelectMultiple si prefieres un desplegable
        label="Seleccionar destinatarios"
    )
    # Campo para el primer mensaje de la conversación
    initial_message = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 3, 'placeholder': 'Escribe el primer mensaje...'}),
        label="Mensaje inicial"
    )

    def __init__(self, *args, **kwargs):
        # El usuario actual se pasa para excluirlo de la lista de destinatarios
        current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)
        if current_user:
            # Filtra el queryset para que el usuario actual no pueda enviarse mensajes a sí mismo
            self.fields['recipients'].queryset = User.objects.exclude(id=current_user.id)

