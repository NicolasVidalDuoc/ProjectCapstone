from django import forms
from .models import Proyecto, Solicitud

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            #'imagen_proyecto': forms.FileInput(attrs={'class': 'form-control'}),
            'nombre_proyecto': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'requisitos': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_termino': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_creacion_proyecto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_actualizacion_proyecto': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }

# Formulario para postular a un proyecto
class PostulacionForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50, required=True)
    apellido = forms.CharField(max_length=50, required=True)

    class Meta:
        model = Solicitud
        fields = ['nombre', 'apellido']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'})
        }