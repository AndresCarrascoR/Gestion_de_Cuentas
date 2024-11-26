from celery import shared_task
from datetime import timedelta
from django.utils.timezone import now
from django.core.mail import send_mail
from django.conf import settings
from facturas.models import FacturaCliente, FacturaProveedor
from .models import Notificacion
import logging

logger = logging.getLogger(__name__)

@shared_task
def notificar_facturas_proximas_vencer():
    logger.info("Iniciando tarea: Notificar facturas próximas a vencer.")
    fecha_limite = now().date() + timedelta(days=3)
    
    try:
        # Facturas de clientes próximas a vencer
        facturas_clientes = FacturaCliente.objects.filter(
            fecha_vencimiento=fecha_limite, 
            estado='pendiente'
        )
        for factura in facturas_clientes:
            Notificacion.objects.create(
                usuario_tipo='cliente',
                usuario_id=factura.cliente.id,
                mensaje=f"Factura {factura.numero_factura} está próxima a vencer",
                link=f"/facturas/{factura.id}"
            )
            enviar_email_notificacion(
                factura.cliente.email,
                f"Factura {factura.numero_factura} está próxima a vencer"
            )

        # Facturas de proveedores próximas a vencer
        facturas_proveedores = FacturaProveedor.objects.filter(
            fecha_vencimiento=fecha_limite, 
            estado='pendiente'
        )
        for factura in facturas_proveedores:
            Notificacion.objects.create(
                usuario_tipo='proveedor',
                usuario_id=factura.proveedor.id,
                mensaje=f"Factura {factura.numero_factura} está próxima a vencer",
                link=f"/facturas/{factura.id}"
            )
            enviar_email_notificacion(
                factura.proveedor.email,
                f"Factura {factura.numero_factura} está próxima a vencer"
            )
    except Exception as e:
        logger.error(f"Error en tarea notificar_facturas_proximas_vencer: {str(e)}")

@shared_task
def notificar_facturas_vencidas():
    logger.info("Iniciando tarea: Notificar facturas vencidas.")
    try:
        # Facturas vencidas de clientes
        facturas_clientes = FacturaCliente.objects.filter(
            fecha_vencimiento__lt=now().date(),
            estado='pendiente'
        )
        for factura in facturas_clientes:
            Notificacion.objects.create(
                usuario_tipo='cliente',
                usuario_id=factura.cliente.id,
                mensaje=f"Factura {factura.numero_factura} está vencida",
                link=f"/facturas/{factura.id}"
            )
            enviar_email_notificacion(
                factura.cliente.email,
                f"Factura {factura.numero_factura} está vencida"
            )

        # Facturas vencidas de proveedores
        facturas_proveedores = FacturaProveedor.objects.filter(
            fecha_vencimiento__lt=now().date(),
            estado='pendiente'
        )
        for factura in facturas_proveedores:
            Notificacion.objects.create(
                usuario_tipo='proveedor',
                usuario_id=factura.proveedor.id,
                mensaje=f"Factura {factura.numero_factura} está vencida",
                link=f"/facturas/{factura.id}"
            )
            enviar_email_notificacion(
                factura.proveedor.email,
                f"Factura {factura.numero_factura} está vencida"
            )
    except Exception as e:
        logger.error(f"Error en tarea notificar_facturas_vencidas: {str(e)}")

def enviar_email_notificacion(email_destino, mensaje):
    try:
        send_mail(
            subject='Notificación de Factura',
            message=mensaje,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email_destino],
            fail_silently=False,
        )
        logger.info(f"Correo enviado a {email_destino}: {mensaje}")
    except Exception as e:
        logger.error(f"Error al enviar email a {email_destino}: {str(e)}")
