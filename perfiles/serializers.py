from rest_framework import serializers
from .models import PerfilEstudiante

class PerfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerfilEstudiante
        fields = (
            'id','nombre','rut','carrera','semestre','email',
            'nota1','nota2','nota3','nota4','promedio'
        )
        read_only_fields = ('id','rut','promedio','nombre')  # nombre solo editable desde admin (ajustar esto mas tarde)
