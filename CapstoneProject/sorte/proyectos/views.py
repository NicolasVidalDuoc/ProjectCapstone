from django.shortcuts import render, redirect, get_object_or_404
from .models import Proyecto, Solicitud
from .forms import ProyectoForm
from django.contrib import messages
from .forms import PostulacionForm
from django.core.mail import send_mail
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required

#--------------------------------------------------------------------------------------------

# Listar Proyectos
def listar_proyecto(request):
    proyectos = Proyecto.objects.all()
    return render(request, "proyectos/listar_proyectos.html", {'proyectos':proyectos})

#--------------------------------------------------------------------------------------------

# Detalle Proyecto
def detalle_proyecto(request, pk):
    proyectos = get_object_or_404(Proyecto, pk=pk)
    return render(request, 'proyectos/detalle_proyecto.html', {'proyectos': proyectos})

#--------------------------------------------------------------------------------------------

# Crear Proyecto
@staff_member_required
def crear_proyecto(request):
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El proyecto ha sido creado correctamente!')
            return redirect('listar_proyectos')
    else:
        form = ProyectoForm()
    return render(request, 'proyectos/crear_proyecto.html', {'form': form})

#--------------------------------------------------------------------------------------------

# Editar Proyecto
@staff_member_required
def editar_proyecto(request, pk):
    proyectos = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        form = ProyectoForm(request.POST, request.FILES, instance=proyectos)
        if form.is_valid():
            form.save()
            messages.success(request, '¡El proyecto ha sido editado correctamente!')
            return redirect('listar_proyectos')
    else:
        form = ProyectoForm(instance=proyectos)
    return render(request, 'proyectos/editar_proyecto.html', {'form': form, 'proyectos': proyectos})

#--------------------------------------------------------------------------------------------

# Eliminar Proyecto
@staff_member_required
def eliminar_proyecto(request, pk):
    proyectos = get_object_or_404(Proyecto, pk=pk)
    if request.method == 'POST':
        proyectos.delete()
        messages.success(request, '¡El proyecto ha sido eliminado correctamente!')
        return redirect('listar_proyectos')
    return render(request, 'proyectos/eliminar_proyecto_confirmar.html', {'proyectos': proyectos})

#--------------------------------------------------------------------------------------------

# Vista para la inscripción de proyectos
@login_required
def inscribir_proyecto(request, proyecto_id):
    proyecto = Proyecto.objects.get(id=proyecto_id)

    if proyecto.cupos_disponibles_proyecto > 0:
        if request.method == 'POST':
            form = PostulacionForm(request.POST)
            if form.is_valid():
                solicitud = form.save(commit=False)
                solicitud.proyecto = proyecto
                solicitud.miembro = request.user
                solicitud.estado = 'pendiente'

                # Verifica si el usuario ya ha postulado al proyecto
                solicitud_existente = Solicitud.objects.filter(proyecto=proyecto, miembro=request.user).first()

                if solicitud_existente is not None:
                    messages.error(request, 'Lo sentimos, pero ya has enviado una solicitud para este proyecto')
                else:
                    solicitud.save()

                    proyecto.cupos_disponibles_proyecto -= 1
                    proyecto.save()
                    messages.success(request, 'Tu solicitud ha sido enviada y será gestionada por nuestra directiva.')
                    send_mail('Confirmación de Solicitud', 'Tu solicitud ha sido recibida y será gestionada por nuestra directiva. Te confirmaremos si fue aceptada o rechazada \
                        por correo. ¡Muchas Gracias!', 'cuentaprueba4326@gmail.com', [request.user.email])
                    return redirect("mis_solicitudes")
        else:
            form = PostulacionForm()
        
        return render(request, 'proyectos/inscripcion_proyecto.html', {'form': form, 'proyecto': proyecto})
    else:
        messages.error(request, 'Lo sentimos, pero ya no hay cupos disponibles para este proyecto.')
        send_mail('Cupos Agotados', 'Lo sentimos, ya no quedan cupos disponibles para este proyecto.', 'cuentaprueba4326@gmail.com', [request.user.email])
        return redirect('mis_solicitudes')
    
# ----------------------------------------------------------------------------------

@staff_member_required
def gestionar_solicitudes(request):
    if not request.user.is_staff:
        return redirect('inicio')
    
    solicitudes = Solicitud.objects.all()

    if request.method == 'POST':
        solicitud_id = request.POST.get('solicitud_id')
        decision = request.POST.get('decision')
        solicitud = Solicitud.objects.get(id=solicitud_id)

        if decision == 'aceptar':
            solicitud.estado = 'aceptada'
            send_mail('¡Solicitud Aceptada!', 'Tu solicitud ha sido aceptada, por lo tanto, puedes participar en este proyecto!', 'cuentaprueba4326@gmail.com', [solicitud.miembro.email])
        elif decision == 'rechazar':
            solicitud.estado = 'rechazada'
            send_mail('¡Solicitud Rechazada!', 'Tu solicitud ha sido rechazada, por lo tanto, no puedes participar en este proyecto!', 'cuentaprueba4326@gmail.com', [solicitud.miembro.email])

        solicitud.save()
        messages.success(request, f'Solicitud {decision.capitalize()} exitosamente.')

    solicitudes_pendientes = Solicitud.objects.filter(estado = 'pendiente')
    solicitudes_aceptadas = Solicitud.objects.filter(estado = 'aceptada')
    solicitudes_rechazadas = Solicitud.objects.filter(estado = 'rechazada')

    return render(request, 'proyectos/gestionar_solicitudes.html', {
        'solicitudes_pendientes': solicitudes_pendientes,
        'solicitudes_aceptadas': solicitudes_aceptadas,
        'solicitudes_rechazadas': solicitudes_rechazadas,
    })

# -----------------------------------------------------------------------------

@login_required
def mis_solicitudes(request):
    solicitudes = Solicitud.objects.filter(miembro = request.user)
    return render(request, 'proyectos/mis_solicitudes.html', {'solicitudes': solicitudes})