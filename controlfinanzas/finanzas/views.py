from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransaccionForm
from .models import Transaccion  
from django.db import models 

@login_required
def vista_principal(request):
    if request.method == 'POST':
        form = TransaccionForm(request.POST)
        if form.is_valid():
            form.save()
            # Redirigir a la misma página para actualizar los cálculos
            return redirect('vista_principal')
    else:
        form = TransaccionForm()

    # Obtener todos los gastos para mostrar en la tabla
    gastos = Transaccion.objects.filter(tipo='Gasto').order_by('-fecha')[:10]

    # Calcular ingresos totales y gastos totales
    ingresos_totales = Transaccion.objects.filter(tipo='Ingreso').aggregate(total=models.Sum('valor'))['total'] or 0
    gastos_totales = Transaccion.objects.filter(tipo='Gasto').aggregate(total=models.Sum('valor'))['total'] or 0
    balance = ingresos_totales - gastos_totales

    context = {
        'form': form,
        'gastos': gastos,
        'ingresos_totales': ingresos_totales,
        'gastos_totales': gastos_totales,
        'balance': balance,
    }
    return render(request, 'finanzas/index.html', context)
