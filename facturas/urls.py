from django.urls import path
from .views import (
    FacturaClienteView,
    ListarFacturasClienteView,
    DetalleFacturaClienteView,
    ActualizarEstadosFacturasView,
)

urlpatterns = [
    path('ver', FacturaClienteView.as_view(), name='facturas'),
    path('listar/', ListarFacturasClienteView.as_view(), name='listar-facturas'),
    path('<int:pk>/', DetalleFacturaClienteView.as_view(), name='detalle-factura'),
    path('actualizar-estados/', ActualizarEstadosFacturasView.as_view(), name='actualizar-estados'),
]