# accounts/urls.py

from django.urls import path
from . import views
app_name = 'accounts'  # Añade esta línea

urlpatterns = [
    path('login/', views.login_request, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_request, name='logout'),
    path('profile/', views.profile_view, name='profile_view'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/password/', views.change_password, name='change_password'),
]