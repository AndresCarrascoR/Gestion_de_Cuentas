from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('admin', 'Administrador'),
        ('accountant', 'Contador'),
        ('manager', 'Gerente'),
    ]
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='manager'  # Puedes cambiar el valor predeterminado según lo que necesites
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"
