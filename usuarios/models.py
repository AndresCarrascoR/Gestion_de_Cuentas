from django.contrib.auth.models import AbstractUser
from django.db import models
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


class Notificacion(models.Model):
    USUARIO_TIPOS = [
        ('cliente', 'Cliente'),
        ('proveedor', 'Proveedor'),
    ]
    usuario_tipo = models.CharField(max_length=10, choices=USUARIO_TIPOS)
    usuario_id = models.PositiveIntegerField()
    mensaje = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)
    leido = models.BooleanField(default=False)
    link = models.URLField(blank=True, null=True)

    def get_usuario(self):
        if self.usuario_tipo == 'cliente':
            return Cliente.objects.get(id=self.usuario_id)
        elif self.usuario_tipo == 'proveedor':
            return Proveedor.objects.get(id=self.usuario_id)

    def __str__(self):
        return f"Notificación para {self.usuario_tipo} {self.usuario_id} - {self.mensaje}"
