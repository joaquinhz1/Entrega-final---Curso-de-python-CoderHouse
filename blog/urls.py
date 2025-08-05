# blog/urls.py

from django.urls import path
from . import views # Importación relativa estándar (debe ser esta)

urlpatterns = [
    path('', views.post_list, name='post_list'), # Corregido: views.post_list y name='post_list'
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('create/', views.create_post, name='create_post'),
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('about/', views.about_me, name='about_me'),
]   