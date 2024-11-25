from celery import shared_task
from .models import FacturaCliente, FacturaProveedor
from datetime import timedelta
from django.utils.timezone import now

@shared_task
def actualizar_estados_facturas():
    """
    Tarea para actualizar automáticamente el estado de las facturas.
    """
    # Actualizar facturas de clientes
    facturas_clientes = FacturaCliente.objects.filter(estado__in=['pendiente', 'vencida'])
    for factura in facturas_clientes:
        factura.actualizar_estado()

    # Actualizar facturas de proveedores
    facturas_proveedores = FacturaProveedor.objects.filter(estado__in=['pendiente', 'vencida'])
    for factura in facturas_proveedores:
        factura.actualizar_estado()


@shared_task
def notificar_facturas_proximas_vencer():
    """
    Envía notificaciones para facturas próximas a vencer (en 3 días).
    """
    fecha_limite = now().date() + timedelta(days=3)

    # Facturas de clientes próximas a vencer
    facturas_clientes = FacturaCliente.objects.filter(fecha_vencimiento=fecha_limite, estado='pendiente')
    for factura in facturas_clientes:
        # Lógica para enviar notificación
        enviar_notificacion(factura.cliente.email, f"Factura {factura.numero_factura} está próxima a vencer")

    # Facturas de proveedores próximas a vencer
    facturas_proveedores = FacturaProveedor.objects.filter(fecha_vencimiento=fecha_limite, estado='pendiente')
    for factura in facturas_proveedores:
        # Lógica para enviar notificación
        enviar_notificacion(factura.proveedor.email, f"Factura {factura.numero_factura} está próxima a vencer")

@shared_task
def notificar_facturas_vencidas():
    """
    Envía notificaciones para facturas vencidas.
    """
    facturas_vencidas_clientes = FacturaCliente.objects.filter(estado='vencida')
    for factura in facturas_vencidas_clientes:
        # Lógica para enviar notificación
        enviar_notificacion(factura.cliente.email, f"Factura {factura.numero_factura} está vencida")

    facturas_vencidas_proveedores = FacturaProveedor.objects.filter(estado='vencida')
    for factura in facturas_vencidas_proveedores:
        # Lógica para enviar notificación
        enviar_notificacion(factura.proveedor.email, f"Factura {factura.numero_factura} está vencida")
