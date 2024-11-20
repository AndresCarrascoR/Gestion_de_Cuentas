from django.urls import path
from .views import AdminOnlyAPIView  # Importa tu vista protegida

urlpatterns = [
    path('admin-only/', AdminOnlyAPIView.as_view(), name='admin_only'),  # Ruta específica de roles
    
        
]
