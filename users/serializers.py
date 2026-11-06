from django.contrib.auth import password_validation
from rest_framework import serializers

from users.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'matricula', 'password', 'is_active', 'is_staff',
        ]
        extra_kwargs = {
            # CORRECCIÓN 1: la contraseña (hash) solo se ESCRIBE, nunca se devuelve.
            'password': {'write_only': True, 'required': False, 'style': {'input_type': 'password'}},
        }

    def validate_password(self, value):
        password_validation.validate_password(value)
        return value

    def validate(self, attrs):
        # La contraseña es obligatoria únicamente al crear
        if self.instance is None and not attrs.get('password'):
            raise serializers.ValidationError({'password': 'La contraseña es obligatoria al crear un usuario.'})
        return attrs

    def create(self, validated_data):
        password = validated_data.pop('password')
        # create_user guarda el hash correctamente (set_password)
        return User.objects.create_user(password=password, **validated_data)

    def update(self, instance, validated_data):
        # CORRECCIÓN 2: la contraseña solo cambia si viene en la petición.
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
