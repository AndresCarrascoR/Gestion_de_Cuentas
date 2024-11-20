from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

# Definir la acción personalizada para activar usuarios
@admin.action(description='Activar usuarios seleccionados')
def activar_usuarios(modeladmin, request, queryset):
    queryset.update(is_active=True)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Configuración de las acciones personalizadas
    actions = [activar_usuarios]

    # Configuración de los campos que se mostrarán en el listado de usuarios
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'role')
    ordering = ('username',)

    # Campos adicionales para la vista de detalle del usuario
    fieldsets = UserAdmin.fieldsets + (
        ('Campos personalizados', {'fields': ('role',)}),
    )

    # Campos para la vista de creación de un nuevo usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Campos personalizados', {'fields': ('role',)}),
    )
