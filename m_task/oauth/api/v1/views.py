from dj_rest_auth.views import LoginView as BaseLoginView
from dj_rest_auth.views import LogoutView
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import OpenApiExample, extend_schema
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView

from .schemas import login_example, login_request_schema, token_response_schema


@extend_schema(
    tags=['Autenticação 🔒'],
    description='Endpoint para autenticação de usuários',
    request=login_request_schema,
    responses={
        200: token_response_schema,
        401: {'description': 'Credenciais inválidas'}
    },
    examples=[
        login_example,
    ]
)
class LoginView(BaseLoginView):
    permission_classes = ()
    authentication_classes = ()

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
        Realiza login do usuário e retorna tokens JWT
        """
        email = request.data.get("email", "").strip()
        username = request.data.get("username", "").strip()
        password = request.data.get("password")

        # Validação dos campos
        if not (email or username):
            return Response(
                {"error": "Email ou username é necessário"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not password:
            return Response(
                {"error": "Senha é necessária"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Email tem precedência sobre username
        login = email if email else username
        request.data["username"] = login

        try:
            # Tenta autenticar o usuário
            user = authenticate(username=login, password=password)
            if not user:
                return Response(
                    {"error": "Credenciais inválidas"},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # Gera tokens JWT
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }, status=status.HTTP_200_OK)
        except ValidationError:
            return Response(
                {
                    "error": "Credenciais inválidas",
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        return response


@extend_schema(
    tags=['Autenticação 🔒'],
    description='Endpoint para logout de usuários',
    responses={
        200: {'description': 'Logout realizado com sucesso'},
        400: {'description': 'Token inválido'},
        401: {'description': 'Não autenticado'}
    },
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {'type': 'string'}
            },
            'required': ['refresh']
        }
    }
)
class LogoutView(LogoutView):
    permission_classes = [IsAuthenticated]

    @csrf_exempt
    def post(self, request):
        return super().post(request)


@extend_schema(
    tags=['Autenticação 🔒'],
    description='Endpoint para renovar o token de acesso',
    responses={
        200: {'description': 'Token renovado com sucesso'},
        401: {'description': 'Token de refresh inválido'}
    },
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'refresh': {'type': 'string'}
            },
            'required': ['refresh']
        }
    },
    examples=[
        OpenApiExample(
            'Sucesso',
            value={
                'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
            },
            status_codes=['200'],
            request_only=False,
        ),
    ]
)
class CustomTokenRefreshView(TokenRefreshView):
    pass
