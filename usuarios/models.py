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
        ('gerente', 'Gerente'),
        ('contador', 'Contador'),
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




class BasePersona(models.Model):
    """
    Clase base para Cliente y Proveedor.
    """
    nombre = models.CharField(max_length=255)  # Nombre o razón social
    direccion = models.TextField(blank=True, null=True)  # Dirección completa
    telefono = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    estado = models.CharField(max_length=20, default="ACTIVO")  # Ejemplo: ACTIVO, INACTIVO
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # No crea una tabla en la base de datos

    def __str__(self):
        return self.nombre
    


# -------------------------
# Modelo de Cliente
# -------------------------
class Cliente(BasePersona):
    dni = models.CharField(max_length=8, unique=True, blank=True, null=True)
    ruc = models.CharField(max_length=11, unique=True, blank=True, null=True)
    fecha_nacimiento = models.DateField(blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    distrito = models.CharField(max_length=100, blank=True, null=True)
    ubigeo = models.CharField(max_length=6, blank=True, null=True)

    def save(self, *args, **kwargs):
        """
        Valida que al menos uno de los campos RUC o DNI esté presente.
        """
        if not self.ruc and not self.dni:
            raise ValueError("Debe especificar al menos un RUC o un DNI para el cliente.")
        super().save(*args, **kwargs)





# -------------------------
# Modelo de Proveedor
# -------------------------
class Proveedor(BasePersona):
    """
    Modelo para proveedores.
    """
    ruc = models.CharField(max_length=11, unique=True)
    linea_negocio = models.CharField(max_length=255, blank=True, null=True)  # Línea de negocio
    condiciones_domicilio = models.CharField(max_length=50, blank=True, null=True)  # Ejemplo: HABIDO
    tipo_persona = models.CharField(max_length=50, blank=True, null=True)  # Ejemplo: PERSONA JURÍDICA
    departamento = models.CharField(max_length=100, blank=True, null=True)
    provincia = models.CharField(max_length=100, blank=True, null=True)
    distrito = models.CharField(max_length=100, blank=True, null=True)
    ubigeo = models.CharField(max_length=6, blank=True, null=True)
    fecha_creacion_ruc = models.DateField(blank=True, null=True)  # Fecha de creación del RUC
    fecha_actualizacion_ruc = models.DateField(blank=True, null=True)

