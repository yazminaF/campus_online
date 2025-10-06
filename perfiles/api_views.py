# perfiles/api_views.py
from rest_framework import viewsets, mixins, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404

from .models import PerfilEstudiante
from .serializers import PerfilSerializer

class PerfilViewSet(mixins.RetrieveModelMixin,
                    mixins.ListModelMixin,
                    mixins.UpdateModelMixin,
                    viewsets.GenericViewSet):
    queryset = PerfilEstudiante.objects.select_related('user')
    serializer_class = PerfilSerializer

    # Autenticación y permisos (JWT) aplicados a TODO el viewset
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # GET /api/perfiles/me/  (+ PUT/PATCH si quieres editarte)
    @action(detail=False, methods=['get', 'put', 'patch'], url_path='me')
    def me(self, request):
        perfil = get_object_or_404(PerfilEstudiante, user=request.user)
        if request.method in ('PUT', 'PATCH'):
            serializer = self.get_serializer(perfil, data=request.data, partial=(request.method == 'PATCH'))
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = self.get_serializer(perfil)
        return Response(serializer.data)

    # GET /api/perfiles/whoami/  (diagnóstico)
    @action(detail=False, methods=['get'], url_path='whoami')
    def whoami(self, request):
        u = request.user
        return Response({
            "authenticated": bool(getattr(u, "is_authenticated", False)),
            "user_id": getattr(u, "id", None),
            "username": getattr(u, "username", None),
            "has_perfil": hasattr(u, "perfil"),
            "perfil_id": getattr(getattr(u, "perfil", None), "id", None),
        })
