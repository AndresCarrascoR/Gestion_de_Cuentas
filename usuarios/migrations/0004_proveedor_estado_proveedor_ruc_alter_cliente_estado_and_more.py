# Generated by Django 5.1.2 on 2024-11-24 07:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0003_alter_customuser_options_customuser_unique_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='proveedor',
            name='estado',
            field=models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')], default='ACTIVO', max_length=10, verbose_name='Estado'),
        ),
        migrations.AddField(
            model_name='proveedor',
            name='ruc',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='RUC'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='estado',
            field=models.CharField(choices=[('ACTIVO', 'Activo'), ('INACTIVO', 'Inactivo')], default='ACTIVO', max_length=10, verbose_name='Estado'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='ruc',
            field=models.CharField(blank=True, max_length=11, null=True, unique=True, verbose_name='RUC'),
        ),
    ]
