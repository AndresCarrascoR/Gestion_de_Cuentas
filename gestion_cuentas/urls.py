from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('usuarios.auth_urls')),  # Para autenticación
    path('api/usuarios/', include('usuarios.urls')),  # Para operaciones con usuarios
    path('api/facturas/', include('facturas.urls')),  # Para operaciones con facturas
    path('api/notificaciones/', include('notificaciones.urls')),  # Para notificaciones
]
