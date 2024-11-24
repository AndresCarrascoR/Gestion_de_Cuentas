from django.urls import path
from .views import (
    AdminOnlyView,
    ManagerView,
    AccountantView,
    ClienteDNIView,
    ClienteRUCView,
    ClienteListCreateView,
    ClienteDetailView,
    ProveedorRUCView,
    ProveedorListCreateView,
    ProveedorDetailView,
)

urlpatterns = [
    # Rutas protegidas por roles
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),  # Ruta para admin
    path('manager/', ManagerView.as_view(), name='manager_view'),  # Ruta para manager
    path('accountant/', AccountantView.as_view(), name='accountant_view'),  # Ruta para accountant

    # Rutas para clientes
    path('clientes/actualizar-ruc/', ClienteRUCView.as_view(), name='actualizar_ruc'),
    path('clientes/actualizar-dni/', ClienteDNIView.as_view(), name='actualizar_dni'),
    path('clientes/', ClienteListCreateView.as_view(), name='cliente_list_create'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),

    # Rutas para proveedores
    path('proveedores/actualizar-ruc/', ProveedorRUCView.as_view(), name='proveedor_actualizar_ruc'),
    path('proveedores/', ProveedorListCreateView.as_view(), name='proveedor_list_create'),
    path('proveedores/<int:pk>/', ProveedorDetailView.as_view(), name='proveedor_detail'),
]
