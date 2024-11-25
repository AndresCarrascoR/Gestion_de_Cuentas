from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from usuarios.permissions import IsAdmin, IsAccountant, IsManager
from rest_framework import status
from .models import FacturaCliente
from .serializers import FacturaClienteSerializer
from .tasks import (
    actualizar_estados_facturas,
    notificar_facturas_proximas_vencer,
    notificar_facturas_vencidas
)

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
    Vista para actualizar estados de facturas llamando a la tarea Celery.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        actualizar_estados_facturas.delay()
        return Response(
            {"message": "Tarea para actualizar estados de facturas enviada al worker."},
            status=status.HTTP_202_ACCEPTED
        )


class NotificarFacturasProximasView(APIView):
    """
    Vista para notificar facturas próximas a vencer llamando a la tarea Celery.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        notificar_facturas_proximas_vencer.delay()
        return Response(
            {"message": "Tarea para notificar facturas próximas a vencer enviada al worker."},
            status=status.HTTP_202_ACCEPTED
        )


class NotificarFacturasVencidasView(APIView):
    """
    Vista para notificar facturas vencidas llamando a la tarea Celery.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        notificar_facturas_vencidas.delay()
        return Response(
            {"message": "Tarea para notificar facturas vencidas enviada al worker."},
            status=status.HTTP_202_ACCEPTED
        )








