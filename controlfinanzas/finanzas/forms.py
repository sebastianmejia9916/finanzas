from django import forms
from .models import Transaccion

class TransaccionForm(forms.ModelForm):
    class Meta:
        model = Transaccion
        fields = ['tipo', 'descripcion', 'valor']
