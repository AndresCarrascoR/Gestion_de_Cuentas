from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin

class AdminOnlyAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "¡Hola, administrador!"})
def home_view(request):
    return HttpResponse("<h1>Bienvenido al sistema de gestión de cuentas</h1>")
# Create your views here.
