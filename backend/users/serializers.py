from django.contrib.auth import password_validation
from django.core.exceptions import ValidationError as DjangoValidationError
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

    def validate_matricula(self, value):
        # Cadena vacía -> NULL, para que varios usuarios sin matrícula no choquen por unicidad
        return value or None

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


class RegisterUserSerializer(serializers.ModelSerializer):
    """Registro público: solo expone campos seguros (nunca is_staff / is_active)."""

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'matricula']
        extra_kwargs = {
            'password': {'write_only': True, 'style': {'input_type': 'password'}},
        }

    def validate_matricula(self, value):
        return value or None

    def validate(self, attrs):
        candidate = User(username=attrs.get('username'), email=attrs.get('email'),
                         first_name=attrs.get('first_name', ''), last_name=attrs.get('last_name', ''))
        try:
            password_validation.validate_password(attrs['password'], user=candidate)
        except DjangoValidationError as exc:
            raise serializers.ValidationError({'password': list(exc.messages)})
        return attrs

    def create(self, validated_data):
        # create_user hashea la contraseña con set_password
        return User.objects.create_user(**validated_data)
