# blog/models.py
from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200) # Asegúrate de que esta línea esté presente
    content = models.TextField() # Asegúrate de que esta línea esté presente
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_publicacion = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True) # Asegúrate de que esta línea esté presente

    def __str__(self):
        return self.title