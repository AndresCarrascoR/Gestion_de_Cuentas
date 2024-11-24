from rest_framework import serializers
from .models import Cliente, Proveedor, FacturaCliente, FacturaProveedor

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = '__all__'

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'



class FacturaClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaCliente
        fields = '__all__'

class FacturaProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacturaProveedor
        fields = '__all__'