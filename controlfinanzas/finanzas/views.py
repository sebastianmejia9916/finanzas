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
            return redirect('vista_principal')
    else:
        form = TransaccionForm()

    # Calcular balance financiero
    ingresos_totales = Transaccion.objects.filter(tipo='Ingreso').aggregate(total=models.Sum('valor'))['total'] or 0
    gastos_totales = Transaccion.objects.filter(tipo='Gasto').aggregate(total=models.Sum('valor'))['total'] or 0
    balance = ingresos_totales - gastos_totales

    context = {
        'form': form,
        'balance': balance,
    }
    return render(request, 'finanzas/index.html', context)
