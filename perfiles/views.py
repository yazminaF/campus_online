from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from .models import PerfilEstudiante

def inicio(request):
    # Caso autenticado: redirige si ya tiene perfil
    if request.user.is_authenticated:
        try:
            perfil = PerfilEstudiante.objects.get(user=request.user)
            return redirect('perfil_detalle', pk=perfil.pk)
        except PerfilEstudiante.DoesNotExist:
            # Mostrar selector SOLO de perfiles sin dueño para vincular
            perfiles = PerfilEstudiante.objects.filter(user__isnull=True).order_by('nombre')
            if request.method == "POST":
                pid = request.POST.get('perfil_id')
                if pid:
                    p = get_object_or_404(PerfilEstudiante, pk=pid, user__isnull=True)
                    p.user = request.user
                    p.save()
                    return redirect('perfil_detalle', pk=p.pk)
            return render(request, 'inicio.html', {'sin_perfil': True, 'perfiles': perfiles})

    # Caso NO autenticado: mostrar login embebido
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.get_user()
        auth_login(request, user)
        return redirect('inicio')
    return render(request, 'inicio.html', {'form': form})

@login_required
def perfil_detalle(request, pk):
    perfil = get_object_or_404(PerfilEstudiante, pk=pk)
    # Seguridad: solo el dueño puede ver su perfil
    if perfil.user != request.user:
        return redirect('inicio')
    return render(request, 'perfiles/perfil_detalle.html', {'perfil': perfil})