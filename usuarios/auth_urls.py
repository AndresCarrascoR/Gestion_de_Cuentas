from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views.auth import VistaRegistroUsuario, VistaCerrarSesion, VistaRecursoProtegido,ListarUsuarios, VistaLogin, validar_token

urlpatterns = [
    path('registrar/', VistaRegistroUsuario.as_view(), name='usuario-registrar'),
    path('token/emergencia/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', VistaCerrarSesion.as_view(), name='logout'),
    path('protegido/', VistaRecursoProtegido.as_view(), name='recurso-protegido'),

    path('usuarios/', ListarUsuarios.as_view(), name='listar_usuarios'),  # Nueva ruta para listar usuarios
    path('login/', VistaLogin.as_view(), name='login'),
    path('validar-token/', validar_token, name='validar_token'),  # Nueva ruta para validar el token
]
