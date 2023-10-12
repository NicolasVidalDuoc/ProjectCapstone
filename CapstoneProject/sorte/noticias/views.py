from django.shortcuts import render, get_object_or_404, redirect
from .models import Noticia
from .forms import NoticiaForm
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Listar Noticias
def listar_noticia(request):
    noticias = Noticia.objects.all()
    return render(request, "noticias/listar_noticia.html", {'noticias': noticias})

# --------------------------------------------------------------------------------------------

# Detalle de actividad
def detalle_noticia(request, pk):
    noticias = get_object_or_404(Noticia, pk=pk)
    return render(request, 'noticias/detalle_noticia.html', {'noticias': noticias})

# --------------------------------------------------------------------------------------------

# Crear actividad
@staff_member_required
def crear_noticia(request):
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Tu noticia ha sido creado con exito')
            return redirect('listar_noticia')
    else:
        form = NoticiaForm()
    return render(request, 'noticias/crear_noticia.html', {'form': form})

# --------------------------------------------------------------------------------------------

# Editar actividad
@staff_member_required
def editar_noticia(request, pk):
    noticias = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        form = NoticiaForm(request.POST, request.FILES, instance=noticias)
        if form.is_valid():
            form.save()
            return redirect('listar_noticia')
    else:
        form = NoticiaForm(instance=noticias)
    return render(request, 'noticias/editar_noticia.html', {'form': form, 'noticias': noticias})

# --------------------------------------------------------------------------------------------

# Eliminar actividad
@staff_member_required
def eliminar_noticia(request, pk):
    noticias = get_object_or_404(Noticia, pk=pk)
    if request.method == 'POST':
        noticias.delete()
        return redirect('listar_noticia')
    return render(request, 'noticias/eliminar_noticia_confirmar.html', {'noticias': noticias})