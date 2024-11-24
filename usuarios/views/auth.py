from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from usuarios.permissions import IsAdmin, IsManager, IsAccountant

class AdminOnlyView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "¡Hola, administrador!"})

# Vista para módulos de estadísticas (gerente)
class ManagerView(APIView):
    permission_classes = [IsAuthenticated, IsManager]

    # Lógica para reportes y estadísticas
    def get(self, request):
        return Response({"message": "¡Hola, gerente!"})

# Vista para módulos financieros (contador)
class AccountantView(APIView):
    permission_classes = [IsAuthenticated, IsAccountant]

    # Lógica para datos contables
    def get(self, request):
        return Response({"message": "¡Hola, contador!"})
        

class FinancialSummaryView(APIView):
    """
    Permite a los contadores y gerentes ver un resumen financiero, pero no editar.
    """
    permission_classes = [IsAuthenticated, IsManager | IsAccountant]

    def get(self, request):
        # Lógica para mostrar un resumen financiero
        return Response({"message": "Resumen financiero"})
