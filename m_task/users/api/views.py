from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import APIException
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework_simplejwt.authentication import JWTAuthentication

from m_task.users.models import User

from .serializers import UserRegistrationSerializer, UserSerializer


class UserViewSet(GenericViewSet):
    queryset = User.objects.select_related().all()
    serializer_class = UserSerializer
    authentication_classes = (JWTAuthentication,)
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == "register":
            return UserRegistrationSerializer
        return self.serializer_class

    def get_permissions(self):
        if self.action == "register":
            return ()
        return super().get_permissions()

    @extend_schema(
        tags=["Usuários 👨‍💻"],
        description="Retorna os dados do usuário autenticado",
        responses={
            200: UserSerializer,
            500: {"description": "Erro interno do servidor"},
        },
    )
    @action(detail=False, methods=["get"])
    def me(self, request):
        """Retorna os dados do usuário autenticado"""
        try:
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        except Exception as e:
            raise APIException(detail=str(e))

    @extend_schema(
        tags=["Usuários 👨‍💻"],
        description="Registra um novo usuário no sistema",
        request=UserRegistrationSerializer,
        responses={
            201: UserRegistrationSerializer,
            400: {"description": "Dados inválidos"},
            500: {"description": "Erro interno do servidor"},
        },
        examples=[
            OpenApiExample(
                "Sucesso",
                value={
                    "email": "user@example.com",
                    "name": "User Name",
                    "password": "strongpassword123",
                    "password_confirm": "strongpassword123",
                },
                status_codes=["201"],
            ),
        ],
    )
    @action(detail=False, methods=["post"])
    def register(self, request):
        """Registra um novo usuário no sistema"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
