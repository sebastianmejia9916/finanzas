from django.urls import path
from . import views

urlpatterns = [
    path('', views.vista_principal, name='vista_principal'),
]
