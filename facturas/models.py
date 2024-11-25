from django.db import models
from usuarios.models import Cliente, Proveedor  # Relacionar con Cliente y Proveedor
from django.utils.timezone import now




# Create your models here.
# -------------------------
# Base para Facturas
# -------------------------
class FacturaBase(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True, verbose_name="Número de factura")
    fecha_emision = models.DateField(default=now, verbose_name="Fecha de emisión")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto total")
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente', verbose_name="Estado")

    class Meta:
        abstract = True

    def actualizar_estado(self):
        """
        Actualiza el estado de la factura basado en la fecha de vencimiento.
        """
        if self.estado != 'pagada' and self.fecha_vencimiento < now().date():
            self.estado = 'vencida'
            self.save()

    def __str__(self):
        return f"Factura {self.numero_factura}"


# -------------------------
# Modelo de Facturas para Clientes
# -------------------------
class FacturaCliente(FacturaBase):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente relacionado")

    def __str__(self):
        return f"{super().__str__()} - Cliente: {self.cliente}"


# -------------------------
# Modelo de Facturas para Proveedores
# -------------------------
class FacturaProveedor(FacturaBase):
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Proveedor relacionado")

    def __str__(self):
        return f"{super().__str__()} - Proveedor: {self.proveedor}"




