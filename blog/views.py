# blog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse # Importa reverse para redirecciones explícitas
from .models import Post
from .forms import PostForm

# Vista para la lista de publicaciones
def post_list(request):
    post_list = Post.objects.all().order_by('-fecha_publicacion')
    message = None
    if not post_list:
        message = "Aún no hay publicaciones. ¡Sé el primero en crear una!"
    # He corregido la plantilla a 'blog/post_list.html' asumiendo que el archivo se llama así.
    # Si tu archivo se llama 'post.list.html', mantén 'blog/post.list.html'.
    return render(request, 'blog/post_list.html', {'posts': post_list, 'message': message})

# VISTA: Para mostrar un post individual
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

# VISTA: Para crear un nuevo post
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(reverse('post_list')) # Redirección usando reverse
    else:
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})

# VISTA: Para editar un post existente
@login_required
def edit_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return redirect(reverse('post_detail', kwargs={'pk': post.pk})) # Redirección usando reverse
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect(reverse('post_detail', kwargs={'pk': post.pk})) # Redirección usando reverse
        else:
            # Manejo del caso en que el formulario no es válido
            return render(request, 'blog/edit_post.html', {'form': form, 'post': post})
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/edit_post.html', {'form': form, 'post': post})

# VISTA: Para eliminar un post
@login_required
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user == post.author:
        post.delete()
    return redirect(reverse('post_list')) # Redirección usando reverse

from django.shortcuts import render
# ... (otras importaciones)

def about_me(request):
    return render(request, 'blog/about_me.html')