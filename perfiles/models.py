from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
# Create your models here.

class PerfilEstudiante(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='perfil',
        null=True, blank=True
    )
    rut = models.CharField(max_length=12, unique=True)
    nombre = models.CharField(max_length=120)
    carrera = models.CharField(max_length=120, blank=True)
    semestre = models.PositiveIntegerField(default=1)
    email = models.EmailField(blank=True)
    nota1 = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('7.0'))]
    )
    nota2 = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('7.0'))]
    )
    nota3 = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('7.0'))]
    )
    nota4 = models.DecimalField(
        max_digits=3, decimal_places=1, null=True, blank=True,
        validators=[MinValueValidator(Decimal('1.0')), MaxValueValidator(Decimal('7.0'))]
    )

    def __str__(self):
        return f"{self.nombre} ({self.rut})"
    
    @property
    def promedio(self):
        vals = [self.nota1, self.nota2, self.nota3, self.nota4]
        nums = [v for v in vals if v is not None]
        if not nums:
            return None
        # promedio a 1 decimal
        return round(sum(nums) / len(nums), 1)



