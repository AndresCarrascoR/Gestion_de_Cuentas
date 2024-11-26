from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Cliente, Proveedor
from django.core.exceptions import PermissionDenied
from django.utils.timezone import now
from django.contrib.admin import SimpleListFilter

# Definir la acción personalizada para activar usuarios
@admin.action(description='Activar usuarios seleccionados')
def activar_usuarios(modeladmin, request, queryset):
    queryset.update(is_active=True)

# Filtro personalizado: Usuarios creados este mes
class CreatedThisMonthFilter(SimpleListFilter):
    title = 'creado este mes'  # Nombre del filtro que se mostrará en el administrador
    parameter_name = 'created_this_month'  # Clave que identifica el filtro en la URL

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Sí'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            start_of_month = now().replace(day=1)
            return queryset.filter(date_joined__gte=start_of_month)
        return queryset

# Registro del modelo CustomUser en el administrador
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Configuración de los campos que se mostrarán en el listado de usuarios
    list_display = ('username', 'email', 'role', 'is_staff', 'is_active', 'last_login')  # Incluye más información
    list_filter = ('role', 'is_staff', 'is_active', CreatedThisMonthFilter)  # Agrega filtros avanzados
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

    # Configuración de las acciones personalizadas
    actions = [activar_usuarios]

    # Validación para restringir la creación de administradores
    def save_model(self, request, obj, form, change):
        if not request.user.role == 'admin' and obj.role == 'admin':
            raise PermissionDenied("No tienes permiso para crear un Administrador.")
        super().save_model(request, obj, form, change)

@admin.action(description="Actualizar datos desde RUC")
def actualizar_desde_ruc(modeladmin, request, queryset):
    token = "TU_TOKEN"
    for cliente in queryset:
        if cliente.ruc:
            cliente.actualizar_desde_ruc(token)

@admin.action(description="Actualizar datos desde DNI")
def actualizar_desde_dni(modeladmin, request, queryset):
    token = "TU_TOKEN"
    for cliente in queryset:
        if cliente.dni:
            cliente.actualizar_desde_dni(token)

@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "ruc", "dni", "direccion", "estado")
    actions = [actualizar_desde_ruc, actualizar_desde_dni]

@admin.register(Proveedor)
class ProveedorAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'direccion', 'telefono', 'email', 'estado')  # Campos a mostrar en la lista
    search_fields = ('nombre', 'ruc')  # Campos por los que se puede buscar
    list_filter = ('estado',)  # Filtros para el panel de administración
    ordering = ('nombre',)  # Orden predeterminado
    fields = ('ruc', 'nombre', 'direccion', 'telefono', 'email', 'estado')  # Campos que se mostrarán en el formulario
    readonly_fields = ('id',)  # Campos de solo lectura


