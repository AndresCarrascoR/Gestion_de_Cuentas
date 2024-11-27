from django.urls import path
from usuarios.views.gerente import DashboardView, ExportarDatosView, ImportarFacturasView
from usuarios.views.auth import AdminOnlyView, ManagerView, AccountantView, FinancialSummaryView
from usuarios.views.clientes import ClienteRUCView, ClienteDNIView, ClienteListCreateView, ClienteDetailView
from usuarios.views.proveedores import ProveedorRUCView, ProveedorListCreateView, ProveedorDetailView
from usuarios.admin_views import ManageUsersView, AuditLogsView, SystemStatsView

urlpatterns = [
    # Admin
    path('admin/tools/', AdminOnlyView.as_view(), name='admin-tools'),
    path('admin/manage-users/', ManageUsersView.as_view(), name='manage-users'),
    path('admin/audit-logs/', AuditLogsView.as_view(), name='audit-logs'),
    path('admin/system-stats/', SystemStatsView.as_view(), name='system-stats'),

    # Gerente
    path('manager/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('manager/exportar/<str:formato>/', ExportarDatosView.as_view(), name='exportar-datos'),
    path('manager/importar/', ImportarFacturasView.as_view(), name='importar-datos'),

    # Contador
    path('accountant/summary/', FinancialSummaryView.as_view(), name='financial-summary'),

    
    # Clientes
    path('clientes/', ClienteListCreateView.as_view(), name='cliente-list-create'),
    path('clientes/<int:pk>/', ClienteDetailView.as_view(), name='cliente-detail'),
        # Rutas para consultas automáticas desde RENIEC
    path('clientes/actualizar-ruc/', ClienteRUCView.as_view(), name='actualizar_ruc'),
    path('clientes/actualizar-dni/', ClienteDNIView.as_view(), name='actualizar_dni'),



    # Proveedores
    path('proveedores/ruc/', ProveedorRUCView.as_view(), name='proveedor-ruc'),
    path('proveedores/', ProveedorListCreateView.as_view(), name='proveedor-list-create'),
    path('proveedores/<int:pk>/', ProveedorDetailView.as_view(), name='proveedor-detail')
]
