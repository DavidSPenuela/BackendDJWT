from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import RegisterUserSerializer, UserSerializer


class UserApiViewSet(ModelViewSet):
    """CRUD de usuarios (solo administradores).

    El hasheo de la contraseña y la lógica de actualización viven en el
    serializer, por lo que POST, PUT y PATCH se comportan igual.
    """
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all().order_by('id')


class UserView(APIView):
    """Datos personales del usuario autenticado (requiere token JWT)."""
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    def get(self, request):
        # El serializer ya no incluye la contraseña en la respuesta
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


class RegisterUserView(CreateAPIView):
    """Registro público de nuevos usuarios (no requiere token)."""
    permission_classes = [AllowAny]
    # Sin autenticación: un token vencido en el header no debe impedir registrarse
    authentication_classes = []
    serializer_class = RegisterUserSerializer
    queryset = User.objects.none()

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'Usuario registrado exitosamente',
            'user': {'username': user.username, 'email': user.email, 'matricula': user.matricula},
        }, status=status.HTTP_201_CREATED)
