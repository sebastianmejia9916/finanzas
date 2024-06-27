from django.urls import path
from . import views
from .views import ReportePDF

urlpatterns = [
    path('', views.vista_principal, name='vista_principal'),
    path('generar-reporte/', ReportePDF.as_view(), name='generar_reporte'),
]
