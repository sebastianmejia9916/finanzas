from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import TransaccionForm
from .models import Transaccion  
from django.db import models 
from wkhtmltopdf.views import PDFTemplateResponse
from django.template.loader import get_template
from django.views.generic import View
from .forms import ReporteForm
import openpyxl
from django.http import HttpResponse

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



class ReporteExcel(View):
    def get(self, request, *args, **kwargs):
        # Obtener las fechas del formulario de reporte
        reporte_form = ReporteForm(request.GET or None)
        if reporte_form.is_valid():
            fecha_inicio = reporte_form.cleaned_data['fecha_inicio']
            fecha_fin = reporte_form.cleaned_data['fecha_fin']

            # Obtener datos de ingresos y gastos en el rango de fechas
            ingresos = Transaccion.objects.filter(tipo='Ingreso', fecha__range=[fecha_inicio, fecha_fin])
            gastos = Transaccion.objects.filter(tipo='Gasto', fecha__range=[fecha_inicio, fecha_fin])

            # Crear un nuevo libro de Excel y una hoja de cálculo
            wb = openpyxl.Workbook()
            ws = wb.active
            ws.title = 'Reporte Financiero'

            # Encabezados de la tabla
            ws.append(['Fecha', 'Descripción', 'Tipo', 'Valor'])

            # Agregar datos de ingresos
            for ingreso in ingresos:
                ws.append([ingreso.fecha, ingreso.descripcion, ingreso.tipo, ingreso.valor])

            # Agregar datos de gastos
            for gasto in gastos:
                ws.append([gasto.fecha, gasto.descripcion, gasto.tipo, gasto.valor])

            # Calcular totales
            ingresos_totales = sum(ingreso.valor for ingreso in ingresos)
            gastos_totales = sum(gasto.valor for gasto in gastos)
            balance = ingresos_totales - gastos_totales

            # Agregar fila con totales
            ws.append(['', 'Total Ingresos', '', ingresos_totales])
            ws.append(['', 'Total Gastos', '', gastos_totales])
            ws.append(['', 'Balance', '', balance])

            # Guardar el libro de Excel en un HttpResponse
            response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename=reporte.xlsx'

            # Guardar el contenido del libro de Excel en el HttpResponse
            wb.save(response)
            return response

        # Manejar caso donde el formulario no es válido
        return redirect('vista_principal')  # Otra acción en caso de formulario no válido