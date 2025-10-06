from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import PerfilEstudiante

@receiver(post_save, sender=User)
def crear_o_asegurar_perfil(sender, instance, created, **kwargs):
    if created:
        PerfilEstudiante.objects.create(
            user=instance,
            nombre=instance.get_full_name() or instance.username,
            rut=f"USR-{instance.id}",  # único, respeta unique=True
            email=instance.email or ""
        )
    else:
        # Si por alguna razón no existe el perfil (usuarios viejos)
        if not hasattr(instance, 'perfil'):
            PerfilEstudiante.objects.create(
                user=instance,
                nombre=instance.get_full_name() or instance.username,
                rut=f"USR-{instance.id}",
                email=instance.email or ""
            )
