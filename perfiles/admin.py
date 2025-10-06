from django.contrib import admin

# Register your models here.
from .models import PerfilEstudiante

@admin.register(PerfilEstudiante)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('nombre','rut','carrera','semestre','email','nota1','nota2','nota3','nota4','promedio')
    search_fields = ('nombre','rut','email')
    list_editable = ('nota1','nota2','nota3','nota4')  # editar en línea (opcional)
