from django.urls import path
from .admin_views import ManageUsersView, AuditLogsView, SystemStatsView
from django.urls import path
from usuarios.views.gerente import DashboardView, ExportarDatosView, ImportarFacturasView
from .views import (
    AdminOnlyView,
    ManagerView,
    AccountantView,
    FinancialSummaryView,
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
    # Herramientas de administrador
    path('api/admin-tools/', AdminOnlyView.as_view(), name='admin_only'),
    # Herramientas de gerente
    path('api/manager-tools/', ManagerView.as_view(), name='manager_view'),  
    # Herramientas de contador
    path('api/accountant-tools/', AccountantView.as_view(), name='accountant_view'),

    # Rutas para clientes
    path('clientes/actualizar-ruc/', ClienteRUCView.as_view(), name='actualizar_ruc'),
    path('clientes/actualizar-dni/', ClienteDNIView.as_view(), name='actualizar_dni'),
    path('clientes/', ClienteListCreateView.as_view(), name='cliente_list_create'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente_detail'),

    # Rutas para proveedores
    path('proveedores/actualizar-ruc/', ProveedorRUCView.as_view(), name='proveedor_actualizar_ruc'),
    path('proveedores/', ProveedorListCreateView.as_view(), name='proveedor_list_create'),
    path('proveedores/<int:pk>/', ProveedorDetailView.as_view(), name='proveedor_detail'),

    # Rutas para gerente
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('exportar/<str:formato>/', ExportarDatosView.as_view(), name='exportar-datos'),
    path('importar/', ImportarFacturasView.as_view(), name='importar-facturas'),

    # ruta para todos
    path('financial-summary/', FinancialSummaryView.as_view(), name='financial-summary'),

    # Rutas de admin
    path('admin/manage-users/', ManageUsersView.as_view(), name='manage-users'),
    path('admin/audit-logs/', AuditLogsView.as_view(), name='audit-logs'),
    path('admin/system-stats/', SystemStatsView.as_view(), name='system-stats'),



]
