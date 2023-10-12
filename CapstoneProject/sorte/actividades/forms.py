from django import forms
from .models import Actividad, Inscripcion

class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = '__all__'
        widgets = {
            'nombre_actividad': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'direccion': forms.TextInput(attrs={'class': 'form-control'}),
            'region': forms.Select(attrs={'class': 'form-control'}),
            'comuna': forms.Select(attrs={'class': 'form-control'}),
            'fecha_actividad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora_inicio': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'hora_termino': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'cupos_disponibles': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class InscripcionForm(forms.ModelForm):
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)

    class Meta:
        model = Inscripcion
        fields = ['nombre', 'apellido']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control'})
        }