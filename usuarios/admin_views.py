from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from usuarios.permissions import IsAdmin
from usuarios.models import CustomUser
from django.contrib.auth.models import Group, Permission

# Vista para gestionar usuarios
class ManageUsersView(APIView):
    """
    Vista para listar, crear y actualizar usuarios.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        # Listar todos los usuarios
        usuarios = CustomUser.objects.all().values('id', 'username', 'email', 'role')
        return Response({"usuarios": list(usuarios)})

    def post(self, request):
        # Crear un nuevo usuario
        data = request.data
        nuevo_usuario = CustomUser.objects.create_user(
            username=data.get("username"),
            email=data.get("email"),
            password=data.get("password"),
            role=data.get("role", "usuario")  # Valor por defecto: usuario
        )
        return Response({"message": f"Usuario {nuevo_usuario.username} creado con éxito."})

    def patch(self, request):
        # Actualizar información de un usuario existente
        data = request.data
        usuario_id = data.get("id")
        try:
            usuario = CustomUser.objects.get(id=usuario_id)
            usuario.username = data.get("username", usuario.username)
            usuario.email = data.get("email", usuario.email)
            usuario.role = data.get("role", usuario.role)
            usuario.save()
            return Response({"message": f"Usuario {usuario.username} actualizado con éxito."})
        except CustomUser.DoesNotExist:
            return Response({"error": "Usuario no encontrado."}, status=404)

# Vista para auditorías
class AuditLogsView(APIView):
    """
    Vista para mostrar logs del sistema.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        # Aquí se agregaría lógica para devolver logs del sistema
        logs = [
            {"timestamp": "2024-11-25T10:00:00Z", "evento": "Inicio de sesión exitoso", "usuario": "admin"},
            {"timestamp": "2024-11-24T14:20:00Z", "evento": "Factura creada", "usuario": "contador"},
        ]
        return Response({"logs": logs})

# Vista para estadísticas avanzadas
class SystemStatsView(APIView):
    """
    Vista para mostrar estadísticas globales del sistema.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        # Estadísticas globales del sistema
        total_usuarios = CustomUser.objects.count()
        total_roles = Group.objects.count()
        total_permisos = Permission.objects.count()

        return Response({
            "total_usuarios": total_usuarios,
            "total_roles": total_roles,
            "total_permisos": total_permisos,
        })
