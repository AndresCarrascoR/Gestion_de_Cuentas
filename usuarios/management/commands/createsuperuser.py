from django.contrib.auth.management.commands.createsuperuser import Command as BaseCommand
from django.core.management import CommandError
from usuarios.models import CustomUser

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Ejecuta el comando original
        super().handle(*args, **options)
        # Asigna el rol 'admin' al superusuario
        username = options.get('username')
        if username:
            try:
                user = CustomUser.objects.get(username=username)
                if user.is_superuser and user.is_staff:
                    user.role = 'admin'  # Asigna el rol de administrador
                    user.save()
                    self.stdout.write(f"Superusuario '{username}' creado con rol 'admin'.")
                else:
                    raise CommandError(f"El usuario '{username}' no es un superusuario.")
            except CustomUser.DoesNotExist:
                raise CommandError(f"No se encontró el usuario '{username}'.")
