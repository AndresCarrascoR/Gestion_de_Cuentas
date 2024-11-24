from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from usuarios.models import Cliente
from usuarios.serializers import ClienteSerializer
from usuarios.utils import consulta_ruc, consulta_dni
from usuarios.permissions import IsAdmin, IsManager, IsAccountant
from rest_framework.permissions import IsAuthenticated



# Consulta de RUC
class ClienteRUCView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        ruc = request.data.get("ruc")
        token = request.data.get("token")

        if not ruc:
            return Response({"error": "El RUC es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        if not token:
            return Response({"error": "El token es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente, created = Cliente.objects.get_or_create(ruc=ruc)
            resultado = cliente.actualizar_desde_ruc(token)
            if "error" in resultado:
                return Response(resultado, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "success": True,
                "message": "Cliente creado." if created else "Cliente actualizado.",
                "data": resultado["datos"],
                "cambios": resultado.get("cambios", []),
                "created": created
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Consulta de DNI
class ClienteDNIView(APIView):
    """
    Consulta DNI y actualiza o crea un cliente en la base de datos.
    Solo para administradores.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        dni = request.data.get("dni")
        token = request.data.get("token")

        if not dni:
            return Response({"error": "El DNI es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        if not token:
            return Response({"error": "El token es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            cliente, created = Cliente.objects.get_or_create(dni=dni)
            datos = cliente.actualizar_desde_dni(token)
            if "error" in datos:
                return Response(datos, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "success": True,
                "message": "Datos procesados correctamente.",
                "data": datos,
                "created": created
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



# Listar y crear clientes
class ClienteListCreateView(generics.ListCreateAPIView):
    """
    Listar todos los clientes o crear nuevos.
    - Admin: CRUD completo.
    - Manager y Accountant: Solo lectura.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsManager | IsAccountant]

    def post(self, request, *args, **kwargs):
        # Solo los administradores pueden crear clientes
        if not request.user.role == 'admin':
            return Response(
                {"detail": "No tienes permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().post(request, *args, **kwargs)


# Ver, actualizar o eliminar clientes
class ClienteDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar un cliente específico.
    - Admin: CRUD completo.
    - Manager y Accountant: Solo lectura.
    """
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    permission_classes = [IsAuthenticated, IsAdmin | IsManager | IsAccountant]

    def update(self, request, *args, **kwargs):
        # Solo los administradores pueden actualizar clientes
        if not request.user.role == 'admin':
            return Response(
                {"detail": "No tienes permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        # Solo los administradores pueden eliminar clientes
        if not request.user.role == 'admin':
            return Response(
                {"detail": "No tienes permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)