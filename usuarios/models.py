from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.timezone import now
from .utils import consulta_ruc, consulta_dni
from django.core.exceptions import ValidationError




# -------------------------
# Modelo de Usuario
# -------------------------
class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('accountant', 'Contador'),
        ('manager', 'Gerente'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='admin'
    )

    # Aseguramos que el username sea único en toda la base de datos
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['username'], name='unique_username')
        ]

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


# -------------------------
# Modelo de Cliente
# -------------------------
class Cliente(models.Model):
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=255, verbose_name="Nombre o Razón Social")
    ruc = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="RUC")
    dni = models.CharField(max_length=8, unique=True, blank=True, null=True, verbose_name="DNI")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo electrónico")
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='ACTIVO',
        verbose_name="Estado"
    )

    def actualizar_desde_ruc(self, token):
        """
        Consulta la API de RUC y actualiza los datos del cliente.
        """
        from usuarios.utils import consulta_ruc  # Evitar importaciones circulares.
        
        if not self.ruc:
            raise ValueError("El RUC es obligatorio para esta operación.")
        
        datos = consulta_ruc(self.ruc, token)
        if "error" not in datos:
            cambios = []
            if self.nombre != datos.get("name", self.nombre):
                self.nombre = datos.get("name", self.nombre)
                cambios.append("nombre")
            if self.direccion != datos.get("address", self.direccion):
                self.direccion = datos.get("address", self.direccion)
                cambios.append("direccion")
            if self.estado != datos.get("status", self.estado):
                self.estado = datos.get("status", self.estado)
                cambios.append("estado")
            
            self.save()
            return {"cambios": cambios, "datos": datos}
        
        return datos

    def actualizar_desde_dni(self, token):
        """
        Consulta la API de DNI y actualiza los datos del cliente.
        """
        from usuarios.utils import consulta_dni  # Evitar importaciones circulares.

        if not self.dni:
            raise ValueError("El DNI es obligatorio para esta operación.")

        datos = consulta_dni(self.dni, token)
        if "error" not in datos:
            cambios = []
            if self.nombre != datos.get("full_name", self.nombre):
                self.nombre = datos.get("full_name", self.nombre)
                cambios.append("nombre")

            self.save()
            return {"cambios": cambios, "datos": datos}

        return datos


# -------------------------
# Modelo de Proveedor
# -------------------------
class Proveedor(models.Model):
    ESTADOS = [
        ('ACTIVO', 'Activo'),
        ('INACTIVO', 'Inactivo'),
    ]

    nombre = models.CharField(max_length=255, unique=True, verbose_name="Nombre del proveedor")
    ruc = models.CharField(max_length=11, unique=True, blank=True, null=True, verbose_name="RUC")
    direccion = models.TextField(blank=True, verbose_name="Dirección")
    telefono = models.CharField(max_length=15, blank=True, verbose_name="Teléfono")
    email = models.EmailField(blank=True, verbose_name="Correo electrónico")
    estado = models.CharField(
        max_length=10,
        choices=ESTADOS,
        default='ACTIVO',
        verbose_name="Estado"
    )

    def actualizar_desde_ruc(self, token):
        """
        Consulta la API de RUC y actualiza los datos del proveedor.
        """
        from usuarios.utils import consulta_ruc  # Evitar importaciones circulares.

        if not self.ruc:
            raise ValueError("El RUC es obligatorio para esta operación.")

        datos = consulta_ruc(self.ruc, token)
        if "error" not in datos:
            cambios = []
            if self.nombre != datos.get("name", self.nombre):
                self.nombre = datos.get("name", self.nombre)
                cambios.append("nombre")
            if self.direccion != datos.get("address", self.direccion):
                self.direccion = datos.get("address", self.direccion)
                cambios.append("direccion")
            if self.estado != datos.get("status", self.estado):
                self.estado = datos.get("status", self.estado)
                cambios.append("estado")
            self.save()
            return {"cambios": cambios, "data": datos}
        return datos

    def save(self, *args, **kwargs):
        """
        Validar que el RUC esté presente.
        """
        if not self.ruc:
            raise ValueError("El RUC es obligatorio para registrar un proveedor.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nombre} ({'RUC: ' + self.ruc if self.ruc else 'Sin RUC'})"


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
