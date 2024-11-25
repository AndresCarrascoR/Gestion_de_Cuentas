from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Establece la configuración de Django para Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gestion_cuentas.settings')

app = Celery('gestion_cuentas')

# Lee la configuración desde settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubre tareas automáticamente en aplicaciones registradas
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
