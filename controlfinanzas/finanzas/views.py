from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def vista_principal(request):
    return render(request, 'finanzas/index.html')