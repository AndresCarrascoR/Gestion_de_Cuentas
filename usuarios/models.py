from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now



#Tabla de Usuarios
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('accountant', 'Contador'),
        ('manager', 'Gerente'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='admin'  # Puedes cambiar el valor predeterminado según lo que necesites
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# Modelo para los Clientes
class Cliente(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre del cliente")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo electrónico")

    def __str__(self):
        return self.nombre

# Modelo para los Proveedores
class Proveedor(models.Model):
    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre del proveedor")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo electrónico")

    def __str__(self):
        return self.nombre

# Modelo para las Facturas de Clientes
class FacturaCliente(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True, verbose_name="Número de factura")
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, verbose_name="Cliente relacionado")
    fecha_emision = models.DateField(default=now, verbose_name="Fecha de emisión")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto total")
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente', verbose_name="Estado")

    def actualizar_estado(self):
        """Actualiza el estado basado en la fecha de vencimiento"""
        if self.estado != 'pagada' and self.fecha_vencimiento < now().date():
            self.estado = 'vencida'
            self.save()

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.cliente}"

# Modelo para las Facturas de Proveedores
class FacturaProveedor(models.Model):
    numero_factura = models.CharField(max_length=50, unique=True, verbose_name="Número de factura")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE, verbose_name="Proveedor relacionado")
    fecha_emision = models.DateField(default=now, verbose_name="Fecha de emisión")
    fecha_vencimiento = models.DateField(verbose_name="Fecha de vencimiento")
    monto_total = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Monto total")
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('pagada', 'Pagada'),
        ('vencida', 'Vencida'),
    ]
    estado = models.CharField(max_length=10, choices=ESTADOS, default='pendiente', verbose_name="Estado")

    def actualizar_estado(self):
        """Actualiza el estado basado en la fecha de vencimiento"""
        if self.estado != 'pagada' and self.fecha_vencimiento < now().date():
            self.estado = 'vencida'
            self.save()

    def __str__(self):
        return f"Factura {self.numero_factura} - {self.proveedor}"


#token de prueba
        #49d400db4cb31a20a95cedc2bec27e533d8debfcfac4530d31b5632e1571e4d5


#
#pip install -r requirements.txt