from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from usuarios.permissions import IsAdmin, IsAccountant, IsManager
from .models import FacturaCliente
from .serializers import FacturaClienteSerializer
from celery import current_app


class FacturaClienteView(ListCreateAPIView):
    queryset = FacturaCliente.objects.all()
    serializer_class = FacturaClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAdmin()]  # Solo administradores pueden crear facturas
        elif self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [IsAdmin() | IsAccountant()]  # Administradores y contadores pueden modificar/eliminar
        return super().get_permissions()


class ListarFacturasClienteView(ListAPIView):
    queryset = FacturaCliente.objects.all()
    serializer_class = FacturaClienteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        estado = self.request.query_params.get('estado')
        if estado:
            return self.queryset.filter(estado=estado)
        return self.queryset


class DetalleFacturaClienteView(RetrieveUpdateDestroyAPIView):
    queryset = FacturaCliente.objects.all()
    serializer_class = FacturaClienteSerializer
    permission_classes = [IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        factura = self.get_object()
        # Restricción: No permitir eliminar si la factura está vinculada a registros contables
        if hasattr(factura, 'registro_contable'):
            return Response(
                {"error": "No se puede eliminar una factura vinculada a registros contables."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().delete(request, *args, **kwargs)


class ActualizarEstadosFacturasView(APIView):
    """
    Vista para actualizar estados de facturas automáticamente
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        current_app.send_task('facturas.tasks.actualizar_estados_facturas')
        return Response(
            {"message": "Tarea de actualización de estados iniciada"},
            status=status.HTTP_202_ACCEPTED
        )










