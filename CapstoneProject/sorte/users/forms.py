from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUSer, Certificado
from django.core.exceptions import ValidationError
from django.utils import timezone
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(min_length=1, max_length=50, required=True)
    last_name = forms.CharField(min_length=1, max_length=50, required=True)
    email = forms.EmailField(label='Correo Electrónico', required=True)
    address = forms.CharField(max_length=200, required=True)
    birthdate = forms.DateField()
    GENDER_CHOICES = (
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('N', 'Prefiero no decirlo'),
    )
    gender = forms.ChoiceField(label='Género', choices=GENDER_CHOICES, required=True, widget=forms.RadioSelect)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox, required=True, 
            error_messages={
            'required': 'Por favor, completa el reCAPTCHA para continuar.'
        })

    # Validador de contraseñas
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Agrega tus propias reglas de validación aquí
        if len(password1) < 8:
            raise ValidationError('La contraseña debe tener al menos 8 caracteres.')

        if not any(char.isdigit() for char in password1):
            raise ValidationError('La contraseña debe contener al menos un número.')

        if not any(char.isalpha() for char in password1):
            raise ValidationError('La contraseña debe contener al menos una letra.')

        if password1 and password2 and password1 != password2:
            raise ValidationError('Las contraseñas no coinciden. Por favor, inténtalo nuevamente.')

        return password2
    
    
    # Validar si el email ya existe en la base de datos
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUSer.objects.filter(email__iexact=email).exists():
            raise ValidationError('Este correo electrónico ya está registrado. Por favor intenta con otro.')
        return email
    
    def clean_gender(self):
        gender = self.cleaned_data.get('gender')
        
        if not gender:
            raise ValidationError("Este campo no puede dejarse vacío. Por favor, selecciona una opción.")
        return gender
    
    def clean_address(self):
        address = self.cleaned_data.get('address')

        if not address:
            raise ValidationError("Este campo no puede dejarse vacío. Por favor, selecciona una opción.")
        return address

    def clean_birthdate(self):
        birthdate = self.cleaned_data.get('birthdate')

        if not birthdate:
            raise ValidationError("Este campo no puede dejarse vacío. Por favor, selecciona una opción.")
        return birthdate       
    

    class Meta:
        model = CustomUSer
        fields = ('rut', 'first_name', 'last_name', 'birthdate', 'address', 'email', 'gender', 'password1', 'password2')


# Formulario para la actualización de los datos de usuarios registrados
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUSer
        fields = ['first_name', 'last_name', 'email']
