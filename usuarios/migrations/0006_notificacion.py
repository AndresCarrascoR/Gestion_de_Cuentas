# Generated by Django 5.1.2 on 2024-11-25 09:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0005_remove_facturaproveedor_proveedor_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('usuario_tipo', models.CharField(choices=[('cliente', 'Cliente'), ('proveedor', 'Proveedor')], max_length=10)),
                ('usuario_id', models.PositiveIntegerField()),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
                ('leido', models.BooleanField(default=False)),
                ('link', models.URLField(blank=True, null=True)),
            ],
        ),
    ]