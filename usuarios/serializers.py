from rest_framework import serializers
from .models import Cliente, Proveedor, CustomUser

class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ['id', 'nombre', 'ruc', 'dni', 'direccion', 'telefono', 'email', 'estado']

    def validate(self, data):
        """
        Valida que al menos uno de los campos RUC o DNI esté presente.
        """
        if not data.get('ruc') and not data.get('dni'):
            raise serializers.ValidationError("Debe proporcionar al menos un RUC o un DNI.")
        return data

    def create(self, validated_data):
        """
        Lógica para crear un cliente priorizando el RUC sobre el DNI.
        """
        ruc = validated_data.get('ruc')
        dni = validated_data.get('dni')

        if ruc:
            cliente, created = Cliente.objects.get_or_create(ruc=ruc, defaults=validated_data)
        elif dni:
            cliente, created = Cliente.objects.get_or_create(dni=dni, defaults=validated_data)
        else:
            raise serializers.ValidationError("Debe proporcionar al menos un RUC o un DNI.")
        return cliente

class ProveedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proveedor
        fields = '__all__'


class SerializadorUsuario(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'password', 'role']

    def validate_role(self, value):
        if value not in ['gerente', 'contador']:
            raise serializers.ValidationError("El rol debe ser 'gerente' o 'contador'.")
        return value

    def create(self, validated_data):
        usuario = CustomUser(**validated_data)
        usuario.set_password(validated_data['password'])
        usuario.save()
        return usuario

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'role']

