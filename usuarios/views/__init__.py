from .auth import AdminOnlyView, ManagerView, AccountantView
from .clientes import ClienteRUCView, ClienteDNIView, ClienteListCreateView, ClienteDetailView, FacturaClienteListCreateView, FacturaClienteDetailView
from .proveedores import ProveedorRUCView, ProveedorListCreateView, ProveedorDetailView, FacturaProveedorListCreateView, FacturaProveedorDetailView

__all__ = [
    "AdminOnlyView",
    "ManagerView",
    "AccountantView",

    "ClienteRUCView",
    "ClienteDNIView",  # Asegúrate de incluir esta línea para evitar errores de importación
    "ClienteListCreateView",
    "ClienteDetailView",

    "ProveedorRUCView",
    "ProveedorListCreateView",
    "ProveedorDetailView",

    "FacturaClienteListCreateView",
    "FacturaClienteDetailView",
    "FacturaProveedorListCreateView",
    "FacturaProveedorDetailView",
    
    
    
]
