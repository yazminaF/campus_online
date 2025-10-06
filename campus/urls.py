"""
URL configuration for campus project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from perfiles.views import inicio, perfil_detalle
from django.contrib.auth.views import LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from perfiles import views  # vistas HTML

# DRF
from rest_framework.routers import DefaultRouter
from perfiles.api_views import PerfilViewSet
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Configuración del router para el API
router = DefaultRouter()
router.register(r'perfiles', PerfilViewSet, basename='perfil')

urlpatterns = [
    path('', inicio, name='inicio'),
    path('perfil/<int:pk>/', perfil_detalle, name='perfil_detalle'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('admin/', admin.site.urls),
    # API Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #API
    path('api/', include(router.urls)),
    # Login/Logout para el browsable API (usa sesiones)
    path('api/auth/', include('rest_framework.urls')),
]
