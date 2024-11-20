from django.urls import path
from .views import AdminOnlyView, ManagerView, AccountantView  # Importa tu vista protegida

urlpatterns = [
    path('admin-only/', AdminOnlyView.as_view(), name='admin_only'),  # Ruta para admin
    path('manager/', ManagerView.as_view(), name='manager_view'),  # Ruta para manager
    path('accountant/', AccountantView.as_view(), name='accountant_view'),  # Ruta para accountant
        
]
