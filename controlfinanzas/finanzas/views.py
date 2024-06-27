from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransaccionForm
from .models import Transaccion  
from django.db import models 
from wkhtmltopdf.views import PDFTemplateResponse
from django.template.loader import get_template
from django.views.generic import View
from django.http import HttpResponse
from .forms import ReporteForm


@login_required
def vista_principal(request):
    form = TransaccionForm(request.POST or None)
    reporte_form = ReporteForm(request.GET or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('vista_principal')

    # Calcular balance financiero
    ingresos_totales = Transaccion.objects.filter(tipo='Ingreso').aggregate(total=models.Sum('valor'))['total'] or 0
    gastos_totales = Transaccion.objects.filter(tipo='Gasto').aggregate(total=models.Sum('valor'))['total'] or 0
    balance = ingresos_totales - gastos_totales

    # Obtener los últimos ingresos y gastos para mostrar
    ingresos = Transaccion.objects.filter(tipo='Ingreso').order_by('-fecha')[:5]
    gastos = Transaccion.objects.filter(tipo='Gasto').order_by('-fecha')[:5]

    context = {
        'form': form,
        'balance': balance,
        'ingresos_totales': ingresos_totales,
        'gastos_totales': gastos_totales,
        'ingresos': ingresos,
        'gastos': gastos,
        'reporte_form': reporte_form,  # Añade el formulario de reporte al contexto
    }
    return render(request, 'finanzas/index.html', context)


class ReportePDF(View):
    def get(self, request, *args, **kwargs):
        # Lógica para obtener datos según el rango de fechas
        fecha_inicio = request.GET.get('fecha_inicio')
        fecha_fin = request.GET.get('fecha_fin')

        # Obtener datos de ingresos y gastos en el rango de fechas
        ingresos = Transaccion.objects.filter(tipo='Ingreso', fecha__range=[fecha_inicio, fecha_fin])
        gastos = Transaccion.objects.filter(tipo='Gasto', fecha__range=[fecha_inicio, fecha_fin])

        # Calcular totales
        ingresos_totales = sum(ingreso.valor for ingreso in ingresos)
        gastos_totales = sum(gasto.valor for gasto in gastos)
        balance = ingresos_totales - gastos_totales

        # Renderizar el template HTML para el PDF
        context = {
            'fecha_inicio': fecha_inicio,
            'fecha_fin': fecha_fin,
            'ingresos': ingresos,
            'gastos': gastos,
            'ingresos_totales': ingresos_totales,
            'gastos_totales': gastos_totales,
            'balance': balance,
        }
        template = get_template('finanzas/reporte_pdf.html')
        html = template.render(context)

        # Generar la respuesta PDF y devolverla
        response = PDFTemplateResponse(request=request, template='finanzas/reporte_pdf.html', filename='reporte.pdf', context=context)
        return response