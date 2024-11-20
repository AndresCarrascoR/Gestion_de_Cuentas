from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAdmin, IsManager, IsAccountant

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
