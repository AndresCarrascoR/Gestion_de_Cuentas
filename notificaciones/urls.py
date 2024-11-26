from django.urls import path
from .views import (
    ListarNotificacionesView,
    NotificarFacturasProximasView,
    NotificarFacturasVencidasView
)

urlpatterns = [
    path('ver', ListarNotificacionesView.as_view(), name='listar-notificaciones'),
    path('notificar-proximas/', NotificarFacturasProximasView.as_view(), name='notificar-proximas'),
    path('notificar-vencidas/', NotificarFacturasVencidasView.as_view(), name='notificar-vencidas'),
]