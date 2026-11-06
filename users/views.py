from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from users.models import User
from users.serializers import UserSerializer


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
