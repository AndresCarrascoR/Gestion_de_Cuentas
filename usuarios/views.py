from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsManager, IsAccountant
from rest_framework import status
from .models import Cliente
from .serializers import ClienteSerializer


class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "¡Hola, administrador!"})

class ManagerView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    def get(self, request):
        return Response({"message": "¡Hola, gerente!"})

class AccountantView(APIView):
    permission_classes = [IsAuthenticated, IsAccountant]

    def get(self, request):
        return Response({"message": "¡Hola, contador!"})


class ClienteRUCView(APIView):
    def post(self, request, *args, **kwargs):
        ruc = request.data.get("ruc")
        if not ruc:
            return Response({"error": "El RUC es obligatorio."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # Lógica para consultar RUC o manejar base de datos
            pass
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"success": "Datos procesados correctamente."}, status=status.HTTP_200_OK)












