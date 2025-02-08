from drf_spectacular.utils import OpenApiExample, inline_serializer
from rest_framework import serializers

# Schemas para request/response
login_request_schema = inline_serializer(
    name='LoginRequest',
    fields={
        'email': serializers.EmailField(),
        'password': serializers.CharField(write_only=True)
    }
)

login_example = OpenApiExample(
    'Login',
    value={
        'email': 'admin@admin.com',
        'password': 'wanilda123'
    },
)

token_response_schema = inline_serializer(
    name='TokenResponse',
    fields={
        'access': serializers.CharField(),
        'refresh': serializers.CharField()
    }
)

# Exemplos
login_success_example = OpenApiExample(
    'Login Sucesso',
    value={
        'access': 'eyJ0eXAiOiJKV1QiLCJhbGc...',
        'refresh': 'eyJ0eXAiOiJKV1QiLCJhbGc...'
    },
    status_codes=['200']
)

login_error_example = OpenApiExample(
    'Erro de Credenciais',
    value={
        'error': 'Credenciais inválidas'
    },
    status_codes=['401']
)
