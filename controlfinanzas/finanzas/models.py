from django.db import models
from django.contrib.auth.models import User

class Transaccion(models.Model):
    TIPOS_CHOICES = (
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto'),
    )

    tipo = models.CharField(max_length=10, choices=TIPOS_CHOICES)
    descripcion = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=13, decimal_places=3)
    fecha = models.DateField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - {self.valor_formateado()} - {self.fecha}"

    def valor_formateado(self):
        return '{:,.3f}'.format(self.valor)
