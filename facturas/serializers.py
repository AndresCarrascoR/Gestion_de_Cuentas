from rest_framework import serializers
from .models import FacturaCliente, FacturaProveedor

class FacturaClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaCliente
        fields = '__all__'
        read_only_fields = ['fecha_emision', 'numero_factura']  # Campos críticos solo de lectura

    def update(self, instance, validated_data):
        # Verifica que el contador no pueda modificar campos críticos
        for field in ['fecha_emision', 'numero_factura']:
            if field in validated_data:
                validated_data.pop(field, None)
        return super().update(instance, validated_data)


class FacturaProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaProveedor
        fields = '__all__'
        read_only_fields = ['fecha_emision', 'numero_factura']

    def update(self, instance, validated_data):
        for field in ['fecha_emision', 'numero_factura']:
            if field in validated_data:
                validated_data.pop(field, None)
        return super().update(instance, validated_data)
