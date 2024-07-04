from django.urls import path
from .views import vista_principal, ReporteExcel  # Asegúrate de importar todas las vistas necesarias

urlpatterns = [
    path('', vista_principal, name='vista_principal'),  # URL para la vista principal
    path('generar-reporte/', ReporteExcel.as_view(), name='generar_reporte'),  # URL para generar el reporte Excel
    # Otros patrones de URL de tu aplicación
]