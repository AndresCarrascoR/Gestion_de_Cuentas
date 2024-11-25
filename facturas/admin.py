from django.contrib import admin
from .models import FacturaCliente, FacturaProveedor

@admin.register(FacturaCliente)
class FacturaClienteAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'cliente', 'monto_total', 'estado', 'fecha_vencimiento')
    list_filter = ('estado', 'fecha_vencimiento')
    search_fields = ('numero_factura', 'cliente__nombre')

@admin.register(FacturaProveedor)
class FacturaProveedorAdmin(admin.ModelAdmin):
    list_display = ('numero_factura', 'proveedor', 'monto_total', 'estado', 'fecha_vencimiento')
    list_filter = ('estado', 'fecha_vencimiento')
    search_fields = ('numero_factura', 'proveedor__nombre')
