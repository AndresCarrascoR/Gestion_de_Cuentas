from django.urls import path
from .views import (
    ListarNotificacionesView,
    NotificarFacturasProximasView,
    NotificarFacturasVencidasView,
)

urlpatterns = [
    path('listar/', ListarNotificacionesView.as_view(), name='listar-notificaciones'),
    path('proximas/', NotificarFacturasProximasView.as_view(), name='notificar-proximas'),
    path('vencidas/', NotificarFacturasVencidasView.as_view(), name='notificar-vencidas'),
]
