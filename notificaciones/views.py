from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Notificacion
from .serializers import NotificacionSerializer
from celery import current_app
import logging

logger = logging.getLogger(__name__)

class ListarNotificacionesView(generics.ListAPIView):
    serializer_class = NotificacionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notificacion.objects.filter(
            usuario_tipo='cliente' if self.request.user.is_cliente else 'proveedor',
            usuario_id=self.request.user.id
        ).order_by('-fecha')

class NotificarFacturasProximasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info("Iniciando tarea manual: Notificar facturas próximas a vencer.")
        current_app.send_task('notificaciones.tasks.notificar_facturas_proximas_vencer')
        return Response({
            "mensaje": "Tarea de notificación de facturas próximas a vencer iniciada"
        })

class NotificarFacturasVencidasView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logger.info("Iniciando tarea manual: Notificar facturas vencidas.")
        current_app.send_task('notificaciones.tasks.notificar_facturas_vencidas')
        return Response({
            "mensaje": "Tarea de notificación de facturas vencidas iniciada"
        })
