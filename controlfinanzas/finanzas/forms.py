from django import forms
from .models import Transaccion

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'descripcion', 'valor']


class ReporteForm(forms.Form):
    fecha_inicio = forms.DateField(label='Fecha de Inicio', widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_fin = forms.DateField(label='Fecha de Fin', widget=forms.DateInput(attrs={'type': 'date'}))