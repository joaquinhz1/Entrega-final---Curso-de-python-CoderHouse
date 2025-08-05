## accounts/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse # Importa reverse para redirecciones explícitas
from .models import Profile
from .forms import CustomUserCreationForm, UserUpdateForm, ProfileUpdateForm

# VISTA PARA EL LOGIN
def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('post_list') # 'post_list' está en el root URLconf, así que no necesita namespace
    else:
        form = AuthenticationForm()
    return render(request, 'blog/login.html', {'form': form})

# VISTA PARA EL REGISTRO
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse('accounts:login')) # Corregido: usa el namespace 'accounts'
    else:
        form = CustomUserCreationForm()
    return render(request, 'blog/register.html', {'form': form})

# VISTA PARA CERRAR SESIÓN
def logout_request(request):
    logout(request)
    return redirect('post_list') # 'post_list' está en el root URLconf, así que no necesita namespace

# VISTA: Para ver el perfil del usuario
@login_required
def profile_view(request):
    return render(request, 'blog/profile_view.html')

# VISTA: Para editar el perfil
@login_required
def edit_profile(request):
    if request.method == 'POST':
        # Asegúrate de pasar request.FILES si ProfileUpdateForm maneja subidas de archivos
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect(reverse('accounts:profile_view')) # Corregido: usa el namespace 'accounts'
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form
    }
    return render(request, 'blog/edit_profile.html', context)

# VISTA: Para cambiar la contraseña
@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('accounts:profile_view')) # Corregido: usa el namespace 'accounts'
    else:
        form = PasswordChangeForm(request.user)
    
    return render(request, 'blog/change_password.html', {'form': form})
