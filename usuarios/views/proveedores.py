from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from usuarios.models import Proveedor
from usuarios.permissions import IsAdmin
from usuarios.serializers import ProveedorSerializer
from rest_framework.permissions import IsAuthenticated
from usuarios.utils import consulta_ruc

# Consulta de RUC
class ProveedorRUCView(APIView):
    """
    Consulta RUC y actualiza o crea un proveedor en la base de datos.
    Solo para administradores.
    """
    permission_classes = [IsAuthenticated, IsAdmin]

    def post(self, request, *args, **kwargs):
        ruc = request.data.get("ruc")
        token = request.data.get("token")

        if not ruc:
            return Response({"error": "El RUC es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        if not token:
            return Response({"error": "El token es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            proveedor, created = Proveedor.objects.get_or_create(ruc=ruc)
            resultado = proveedor.actualizar_desde_ruc(token)

            if "error" in resultado:
                return Response(resultado, status=status.HTTP_400_BAD_REQUEST)

            return Response({
                "success": True,
                "message": "Datos procesados correctamente.",
                "data": resultado["data"],
                "cambios": resultado["cambios"],
                "created": created
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



class ProveedorListCreateView(generics.ListCreateAPIView):
    """
    Listar o crear proveedores.
    - Admin: CRUD.
    - Contador y Gerente: Solo lectura.
    """
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def post(self, request, *args, **kwargs):
        if not request.user.role == 'admin':
            return Response(
                {"detail": "No tienes permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().post(request, *args, **kwargs)


class ProveedorDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    Ver, actualizar o eliminar un proveedor específico.
    - Admin: CRUD.
    - Contador y Gerente: Solo lectura.
    """
    queryset = Proveedor.objects.all()
    serializer_class = ProveedorSerializer

    def update(self, request, *args, **kwargs):
        if not request.user.role == 'admin':
            return Response(
                {"detail": "No tienes permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if not request.user.role == 'admin':
            return Response(
                {"detail": "No tienes permiso para realizar esta acción."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().destroy(request, *args, **kwargs)
