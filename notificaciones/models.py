from django.db import models
from usuarios.models import Cliente, Proveedor
import logging

logger = logging.getLogger(__name__)

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
            try:
                return Cliente.objects.get(id=self.usuario_id)
            except Cliente.DoesNotExist:
                logger.error(f"Cliente con ID {self.usuario_id} no encontrado.")
        elif self.usuario_tipo == 'proveedor':
            try:
                return Proveedor.objects.get(id=self.usuario_id)
            except Proveedor.DoesNotExist:
                logger.error(f"Proveedor con ID {self.usuario_id} no encontrado.")

    def __str__(self):
        return f"Notificación para {self.usuario_tipo} {self.usuario_id} - {self.mensaje}"
