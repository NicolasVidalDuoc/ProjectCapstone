from django.http import HttpResponse
from .models import CustomUSer, Certificado
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm, UserProfileForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.template.loader import get_template
import io
from reportlab.pdfgen import canvas


@login_required
def profile_user(request):
    return render(request, 'authenticate/profile_user.html')

@login_required
def update_profile_user(request):
    user = request.user

    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile_user')
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'authenticate/update_profile_user.html', {'form': form})


# Vista para el Inicio de sesión del usuario
def login_user(request):
    if request.method == "POST":
        rut = request.POST['rut']
        password = request.POST['password']
        user = authenticate(request, rut=rut, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, ("¡Sesión iniciada correctamente!"))
            return redirect('inicio')
        else:
            messages.error(request, ("¡No es posible iniciar la sesión, por favor comprueba los campos Rut, Contraseña y debes aceptar el Captcha!"))
            return redirect('login')
    else:
        return render(request, 'authenticate/login.html', {})


# Vista para el Cierre de sesión del usuario
@login_required
def logout_user(request):
    logout(request)
    messages.success(request, ("¡Has cerrado la sesión correctamente!"))
    return redirect('inicio')


# Vista para la verificación de la cuenta mediante el correo electrónico del miembro
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Gracias por verificar tu correo electrónico. Ahora puedes iniciar sesión con tu cuenta en SORTE.")
        return redirect('login')
    else:
        messages.error(request, "La verificación ha fallado.")

    return redirect('inicio')


# Vista para la activación del email
def activeEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("authenticate/activate_account.html", {
        'user': user.first_name and user.last_name,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        'protocol': 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f'Estimado <b>{user}</b>, vaya a la bandeja de entrada de su correo electrónico <b>{to_email}</b> y haga clic en \
        Recibí el enlace de activación para confirmar y completar el registro. <b>Nota:</b> Revise su carpeta de spam.')
    else:
        messages.error(request, f'Problema al enviar el correo electrónico a {to_email}, verifique si lo escribió correctamente.')


# Vista para el Registro del usuario
def register_user(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False) # Guardar el usuario recién registrado
            user.is_active=False
            user.save()
            activeEmail(request, user, form.cleaned_data.get('email'))
            return redirect('inicio')
    else:
        form = CustomUserCreationForm()

    return render(request, 'authenticate/register_user.html', {'form': form})


# Vista para generar certificados de residencia de un mimebro de la JDV
def generar_certificado(request):
    user = request.user

    # Verifica si el usuario ya tiene un certificado
    certificado, created = Certificado.objects.get_or_create(usuario=user)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{user.username}_certificado_residencia.pdf"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)

    # Personaliza el contenido del certificado con información del usuario
    p.drawString(100, 800, f"Certificado de Residencia para {user.rut} que acredita que vive en la comuna de Isla de Maipo")
    p.drawString(100, 780, f"Fecha de Emisión: {certificado.fecha_emision.strftime('%Y-%m-%d')}")

    p.showPage()
    p.save()

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response