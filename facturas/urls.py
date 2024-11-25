from django.urls import path
from .views import (
    ActualizarEstadosFacturasView,
    NotificarFacturasProximasView,
    NotificarFacturasVencidasView,
    FacturaClienteView, 
    DetalleFacturaClienteView
)


urlpatterns = [

    path('actualizar-estados/', ActualizarEstadosFacturasView.as_view(), name='actualizar_estados'),
    path('notificar-proximas/', NotificarFacturasProximasView.as_view(), name='notificar_proximas'),
    path('notificar-vencidas/', NotificarFacturasVencidasView.as_view(), name='notificar_vencidas'),

    path('facturas-clientes/', FacturaClienteView.as_view(), name='facturas-clientes'),
    path('facturas-clientes/<int:pk>/', DetalleFacturaClienteView.as_view(), name='detalle-factura-cliente'),

]