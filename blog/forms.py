# blog/forms.py

from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control text-green bg-secondary border-secondary', # Añadido text-white, bg-secondary, border-secondary
                'placeholder': 'Título del Post'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control text-red bg-secondary border-secondary', # Añadido text-white, bg-secondary, border-secondary
                'rows': 10,
                'placeholder': 'Contenido del Post'
            }),
            # No se necesita un widget específico para ImageField aquí, Django lo maneja bien
        }

