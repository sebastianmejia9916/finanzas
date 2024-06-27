from django.db import models

class Transaccion(models.Model):
    TIPOS_CHOICES = (
        ('Ingreso', 'Ingreso'),
        ('Gasto', 'Gasto'),
    )

    tipo = models.CharField(max_length=10, choices=TIPOS_CHOICES)
    descripcion = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.tipo} - {self.descripcion} - {self.valor} - {self.fecha}"
