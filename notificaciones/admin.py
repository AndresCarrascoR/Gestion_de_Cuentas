from django.contrib import admin
from .models import Notificacion

@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ('usuario_tipo', 'usuario_id', 'mensaje', 'fecha', 'leido', 'link')
    list_filter = ('usuario_tipo', 'leido', 'fecha')
    search_fields = ('mensaje', 'usuario_id', 'link')
