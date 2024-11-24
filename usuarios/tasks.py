from celery import shared_task
from .models import FacturaCliente, FacturaProveedor
from django.utils.timezone import now

@shared_task
def actualizar_facturas_vencidas():
    # Actualiza las facturas de clientes
    facturas_clientes = FacturaCliente.objects.all()
    for factura in facturas_clientes:
        if factura.estado != 'pagada' and factura.fecha_vencimiento < now().date():
            factura.estado = 'vencida'
            factura.save()

    # Actualiza las facturas de proveedores
    facturas_proveedores = FacturaProveedor.objects.all()
    for factura in facturas_proveedores:
        if factura.estado != 'pagada' and factura.fecha_vencimiento < now().date():
            factura.estado = 'vencida'
            factura.save()

    return "Facturas actualizadas correctamente"
