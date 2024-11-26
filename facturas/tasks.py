from celery import shared_task
from .models import FacturaCliente, FacturaProveedor


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



