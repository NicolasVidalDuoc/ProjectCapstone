from django.shortcuts import render, get_object_or_404, redirect
from .models import Actividad, Inscripcion
from .forms import ActividadForm, InscripcionForm
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from django.contrib import messages
from django.core.paginator import Paginator

# ----------------------------------------------------------------------

# Listar actividades
def listar_actividad(request):
    actividades = Actividad.objects.all()  
    return render(request, "actividades/listar_actividad.html", {'actividades':actividades})

# ----------------------------------------------------------------------

# Detalle de actividad
def detalle_actividad(request, pk):
    actividades = get_object_or_404(Actividad, pk=pk)
    return render(request, 'actividades/detalle_actividad.html', {'actividades': actividades})

# ----------------------------------------------------------------------

# Crear actividad
@staff_member_required
def crear_actividad(request):
    if request.method == 'POST':
        form = ActividadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡La actividad ha sido creada con éxito!')
            return redirect('listar_actividad')
    else:
        form = ActividadForm()
    return render(request, 'actividades/crear_actividad.html', {'form': form})

# ---------------------------------------------------------------------

# Editar actividad
@staff_member_required
def editar_actividad(request, pk):
    actividades = get_object_or_404(Actividad, pk=pk)
    if request.method == 'POST':
        form = ActividadForm(request.POST, request.FILES, instance=actividades)
        if form.is_valid():
            form.save()
            messages.success(request, '¡La actividad ha sido editada con éxito!')
            return redirect('listar_actividad')
    else:
        form = ActividadForm(instance=actividades)
    return render(request, 'actividades/editar_actividad.html', {'form': form, 'actividades': actividades})

# --------------------------------------------------------------------

# Eliminar actividad
@staff_member_required
def eliminar_actividad(request, pk):
    actividades = get_object_or_404(Actividad, pk=pk)
    actividades.delete()
    return redirect(to='listar_actividad')

# ---------------------------------------------------------------------------------------------------------------------------

# Vista para la inscripción de actividades
@login_required
def inscribir_actividad(request, actividad_id):
    actividad = Actividad.objects.get(id=actividad_id)

    if actividad.cupos_disponibles > 0:
        if request.method == 'POST':
            form = InscripcionForm(request.POST)
            if form.is_valid():
                inscripcion = form.save(commit=False)
                inscripcion.actividad = actividad
                inscripcion.miembro = request.user
                inscripcion.estado = 'pendiente'

                # Verifica si el usuario ya ha postulado a la actividad
                inscripcion_existente = Inscripcion.objects.filter(actividad=actividad, miembro=request.user).first()

                if inscripcion_existente is not None:
                    messages.error(request, 'Lo sentimos, pero ya has enviado una solicitud para esta actividad')
                else:
                    inscripcion.save()

                    actividad.cupos_disponibles -= 1
                    actividad.save()
                    messages.success(request, 'Tu solicitud ha sido enviada y será gestionada por nuestra directiva.')
                    send_mail('Confirmación de Inscripción', 'Tu inscripción ha sido recibida y será gestionada por nuestros administradores. Te confirmaremos si fue aceptada o rechazada por correo. ¡Muchas Gracias!', 'cuentaprueba4326@gmail.com', [request.user.email])
                    return redirect('listar_actividad')
        else:
            form = InscripcionForm()

        return render(request, 'actividades/inscribir_actividad.html', {'form': form, 'actividad': actividad})
    else:
        messages.error(request, 'Lo sentimos, pero ya no hay cupos disponibles para esta actividad.')
        send_mail('Cupos Agotados', 'Lo sentimos, no hay cupos disponibles para esta actividad.', 'cuentaprueba4326@gmail.com', [request.user.email])
        return redirect('listar_actividad')

# ---------------------------------------------------------------------------------------------------------------------------

# Vista para la gestión de inscripciones a las actividades por parte del admin
@staff_member_required
def gestionar_inscripciones(request):
    if not request.user.is_staff:
        return redirect('inicio')

    inscripciones = Inscripcion.objects.all()

    if request.method == 'POST':
        inscripcion_id = request.POST.get('inscripcion_id')
        decision = request.POST.get('decision')
        inscripcion = Inscripcion.objects.get(id=inscripcion_id)

        if decision == 'aceptar':
            inscripcion.estado = 'aceptada'
            send_mail('Inscripción Aceptada', 'Tu Inscripción ha sido aceptada, por lo tanto, puedes participar en nuestra actividad!', 'cuentaprueba4326@gmail.com', [inscripcion.miembro.email])
        elif decision == 'rechazar':
            inscripcion.estado = 'rechazada'
            send_mail('Inscripción Rechazada', 'Tu Inscripción ha sido rechazada, por lo tanto, no puedes participar en nuestra actividad!', 'cuentaprueba4326@gmail.com', [inscripcion.miembro.email])

        inscripcion.save()
        messages.success(request, f'Inscripción {decision.capitalize()} exitosamente.')

    inscripciones_pendientes = Inscripcion.objects.filter(estado='pendiente')
    inscripciones_aceptadas = Inscripcion.objects.filter(estado='aceptada')
    inscripciones_rechazadas = Inscripcion.objects.filter(estado='rechazada')

    return render(request, 'actividades/gestionar_inscripciones.html', {
        'inscripciones_pendientes': inscripciones_pendientes,
        'inscripciones_aceptadas': inscripciones_aceptadas,
        'inscripciones_rechazadas': inscripciones_rechazadas,
    })

# --------------------------------------------------------------------------------------------------------------------------------

# Vista para que el usuario miembro pueda ver sus solicitudes
@login_required
def mis_solicitudes_miembro(request):
    inscripciones = Inscripcion.objects.filter(miembro=request.user)
    return render(request, 'actividades/mis_solicitudes_miembro.html', {'inscripciones': inscripciones})

# --------------------------------------------------------------------------------------------------------------------------------